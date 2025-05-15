from flask import Flask, request
from telegram import Update
from telegram.ext import Application
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "ok"
