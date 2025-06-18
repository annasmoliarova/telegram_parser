from pyrogram import Client
from pyrogram.types import Message
import json
from datetime import datetime
import os

# Замените на свои данные
api_id = 12345 # YOUR API ID
api_hash = 'XXXX' # YOUR API HASH in ''

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def extract_message_data(message: Message, app: Client):
    media_type = None
    local_file = None

    if message.photo:
        media_type = "photo"
        #local_file = app.download_media(message, file_name=DOWNLOAD_FOLDER + "/")
    elif message.video:
        media_type = "video"
        #local_file = app.download_media(message, file_name=DOWNLOAD_FOLDER + "/")
    elif message.document:
        media_type = "document"
        #local_file = app.download_media(message, file_name=DOWNLOAD_FOLDER + "/")
    elif message.voice:
        media_type = "voice"
    elif message.animation:
        media_type = "animation"
    elif message.poll:
        media_type = "poll"

    total_reactions = 0
    if message.reactions and message.reactions.reactions:
        total_reactions = sum(reaction.count for reaction in message.reactions.reactions)

    repost = None
    if message.forward_from_chat:
        repost = message.forward_from_chat.title

    return {
        "id": message.id,
        "date": message.date.isoformat(),
        "text": message.text or message.caption,
        "media_type": media_type,
        "local_file": local_file,
        "views": message.views,
        "forwards": message.forwards,
        "reactions": total_reactions,
        "repost": repost

    }


def main():
    with Client("telegram_downloader", api_id=api_id, api_hash=api_hash) as app:
        url = input("Введите ссылку на канал или чат: ").strip()
        channel = app.get_chat(url)

        print(f"Скачиваю сообщения из: {channel.title}")
        messages = []
        for message in app.get_chat_history(channel.id):
            messages.append(extract_message_data(message, app))
            print(extract_message_data(message, app))

        file_name = url.split("/")[-1] + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"Готово. Данные сохранены в {file_name}")


if __name__ == "__main__":
    main()