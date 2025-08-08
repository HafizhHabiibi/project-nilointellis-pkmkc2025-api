import requests
from flask import current_app
from pymongo import MongoClient
from datetime import datetime

def get_db():
    client = MongoClient(current_app.config["MONGO_URI"])
    return client["nilo"]

def save_chat_id(chat_id):
    db = get_db()
    collection = db["chat_id_collection"]
    if not collection.find_one({"chat_id":chat_id}):
        collection.insert_one({
            "chat_id": chat_id,
            "joined_at": datetime.utcnow()
        })

def get_chat_id():
    db = get_db()
    collection = db["chat_id_collection"]
    return [doc["chat_id"] for doc in collection.find()]

def send_notif(message):
    token = current_app.config['TELEGRAM_BOT_TOKEN']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_ids = get_chat_id()

    for chat_id in chat_ids:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': "Markdown"
        }
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Gagal kirim ke {chat_id}:", e)

def sokap(chat_id):
    """Respon ketika user memulai bot dengan /start."""
    save_chat_id(chat_id)
    pesan = (
        "*👋📡 Selamat datang di NiloIntellisBOT!*\n\n"
        "PKM-KC Universitas Teknologi Yogyakarta 2025"
    )
    token = current_app.config['TELEGRAM_BOT_TOKEN']
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': pesan,
        'parse_mode': "Markdown"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim sambutan ke {chat_id}:", e)