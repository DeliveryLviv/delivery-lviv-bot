import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
URL = "https://tamadakyma.pythonanywhere.com"  

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")

print(response.status_code)
print(response.text)
