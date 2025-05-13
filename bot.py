import os
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)

TOKEN = "7333032712:AAGDIXKZPa-iBabPRL2YaWI9_oeL5gTaA1Y"
ADMIN_CHAT_ID = 915669253
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://delivery-lviv-bot.onrender.com{WEBHOOK_PATH}"

NAME, SERVICE, LOADERS, ADDRESS, TIME, PHONE = range(6)

service_keyboard = [
    ["\U0001F3E2 Квартирний та офісний переїзд"],
    ["\U0001F4E6 Перевезення збірних вантажів"],
    ["\U0001F9F1 Перевезення буд матеріалів"],
    ["\u26A0\uFE0F Перевезення негабаритних вантажів"],
    ["\U0001F3D7 Вивіз будсміття"],
    ["\u2744\uFE0F Перевезення вантажів рефрижиратором"],
    ["\U0001F69B Доставка меблів, техніки, інше"],
    ["\U0001F3EC Для магазинів: доставка продуктів, товарів"],
    ["\U0001F37D Для клінік, ресторанів, кавʼярень: перевезення продуктів у холодильнику"],
    ["\U0001F6D2 Для онлайн-магазинів (логістика)"]
]

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

@app.post(WEBHOOK_PATH)
def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Як вас звати?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "Оберіть послугу:",
        reply_markup=ReplyKeyboardMarkup(service_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text
    await update.message.reply_text(
        "Чи потрібні вантажники? Якщо так — вкажіть кількість. Якщо ні — напишіть 'ні'.",
        reply_markup=ReplyKeyboardRemove()
    )
    return LOADERS

async def get_loaders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["loaders"] = update.message.text
    await update.message.reply_text("Вкажіть адресу перевезення (звідки і куди):")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("На який день і час потрібне перевезення?")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("Будь ласка, залиште свій номер телефону:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    msg = f"""\U0001F4E6 НОВЕ ЗАМОВЛЕННЯ!

\U0001F464 Ім’я: {context.user_data['name']}
\U0001F6E0 Послуга: {context.user_data['service']}
\U0001F46C Вантажники: {context.user_data['loaders']}
\U0001F4CD Адреса: {context.user_data['address']}
\U0001F552 Час: {context.user_data['time']}
\U0001F4DE Телефон: {context.user_data['phone']}"""

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
    await update.message.reply_text("Дякуємо! Ми зв’яжемося з вами протягом 10 хвилин.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Замовлення скасовано.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
        LOADERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_loaders)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

application.add_handler(conv_handler)

if __name__ == '__main__':
    import asyncio
    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("Webhook встановлено")
    asyncio.run(run())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
