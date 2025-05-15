import telebot

TOKEN = '7333032712:AAGDIXKZPa-iBabPRL2YaWI9_oeL5gTaA1Y'
WEBHOOK_URL = 'https://your-render-app.onrender.com/' + TOKEN

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
