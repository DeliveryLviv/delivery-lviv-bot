import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("7333032712:AAGDIXKZPa-iBabPRL2YaWI9_oeL5gTaA1Y")
URL = "https://tamadakyma.pythonanywhere.com"  

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")

print(response.status_code)
print(response.text)
