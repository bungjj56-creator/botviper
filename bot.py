import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")

SOURCE_CHANNEL_ID = 1406885291524096031
TARGET_CHANNEL_ID = 1433021722269061120

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def translate_text(text, target_lang):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return None

@bot.event
async def on_ready():
    print(f"✅ เข้าสู่ระบบเป็น {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == SOURCE_CHANNEL_ID:
        translated_text = translate_text(message.content, 'id')
        if translated_text:
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(f"**{message.author.display_name}**: {translated_text}")
                print(f"🌐 ไทย ➜ อินโด: {translated_text}")

    elif message.channel.id == TARGET_CHANNEL_ID:
        translated_text = translate_text(message.content, 'th')
        if translated_text:
            source_channel = bot.get_channel(SOURCE_CHANNEL_ID)
            if source_channel:
                await source_channel.send(f"**{message.author.display_name}**: {translated_text}")
                print(f"🌐 อินโด ➜ ไทย: {translated_text}")

    await bot.process_commands(message)

app = Flask("")

@app.route("/")
def home():
    return "Bot is running."

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: TOKEN is empty. Set the TOKEN environment variable.")
    else:
        threading.Thread(target=run_flask).start()
        bot.run(TOKEN)
