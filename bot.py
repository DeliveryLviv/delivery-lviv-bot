
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))


# Кроки
NAME, SERVICE, LOADERS, ADDRESS, TIME, PHONE = range(6)

# Клавіатура послуг
service_keyboard = [
    ["🏢 Квартирний та офісний переїзд"],
    ["📦 Перевезення збірних вантажів"],
    ["🧱 Перевезення буд матеріалів"],
    ["⚠️ Перевезення негабаритних вантажів"],
    ["🏗 Вивіз будсміття"],
    ["❄️ Перевезення вантажів рефрижиратором"],
    ["🚛 Доставка меблів, техніки, інше"],
    ["🏬 Для магазинів: доставка продуктів, товарів"],
    ["🍽 Для клінік, ресторанів, кавʼярень"],
    ["🛒 Для онлайн-магазинів (логістика)"]
]

start_keyboard = [["🚀 Зробити замовлення"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Натисніть кнопку нижче, щоб почати оформлення замовлення.",
        reply_markup=ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🚀 Зробити замовлення":
        await update.message.reply_text("Привіт! Як вас звати?", reply_markup=ReplyKeyboardRemove())
        return NAME
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "Оберіть послугу:",
        reply_markup=ReplyKeyboardMarkup(service_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text
    await update.message.reply_text("Чи потрібні вантажники? Якщо так — вкажіть кількість. Якщо ні — напишіть 'ні'.",
                                    reply_markup=ReplyKeyboardRemove())
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
    msg = f"""📦 НОВЕ ЗАМОВЛЕННЯ!

👤 Ім’я: {context.user_data['name']}
🛠 Послуга: {context.user_data['service']}
🧍‍♂️ Вантажники: {context.user_data['loaders']}
📍 Адреса: {context.user_data['address']}
⏰ Час: {context.user_data['time']}
📞 Телефон: {context.user_data['phone']}"""

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
    await update.message.reply_text(
        "Дякуємо! Ми зв’яжемося з вами протягом 10 хвилин.",
        reply_markup=ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
    )
    return NAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Замовлення скасовано.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

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
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("✅ Бот запущено через polling")
    app.run_polling()

if __name__ == "__main__":
    main()
