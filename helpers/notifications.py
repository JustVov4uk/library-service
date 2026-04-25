import requests
from decouple import config


def send_telegram_notifications(text: str):
    token = config("TELEGRAM_BOT_TOKEN")
    chat_id = config("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})
