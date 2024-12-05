from functools import wraps
from io import BytesIO
import random
import re
import string

from sqlalchemy.ext.asyncio import AsyncSession
from quart import g, redirect, url_for
import requests

from core.db import AsyncSessionLocal
from core.settings import settings
from core.bot_setup import bot


def get_image_url(file_id: str) -> str:
    """Функция для получения URL изображения по file_id"""
    url = f"https://api.telegram.org/bot{settings.bot_token}/getFile?file_id={file_id}"
    response = requests.get(url)
    result = response.json()
    if result["ok"]:
        file_path = result["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{settings.bot_token}/{file_path}"
    return


def send_image_to_telegram(image_data: bytes) -> str:
    """
    Отправляет изображение (в формате байтов) на сервер Telegram и возвращает file_id.
    Также удаляет сообщение, которое бот отправляет с изображением.
    """
    url = f"https://api.telegram.org/bot{settings.bot_token}/sendPhoto"
    files = {"photo": ("image.jpg", BytesIO(image_data), "image/jpeg")}
    data = {"chat_id": settings.telegram_chat_ids}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    if result["ok"]:
        file_id = result["result"]["photo"][0]["file_id"]
        message_id = result["result"]["message_id"]
        delete_url = (
            f"https://api.telegram.org/bot{settings.bot_token}/deleteMessage"
        )
        delete_data = {
            "chat_id": settings.telegram_chat_ids,
            "message_id": message_id,
        }
        requests.post(delete_url, data=delete_data)
        return file_id
    return


def db_session(func):
    """Декоратор для создания сессий БД."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "db_session" not in g:
            g.db_session = AsyncSessionLocal()
        db = g.get("db_session")
        try:
            return await func(db, *args, **kwargs)
        finally:
            if "db_session" in g:
                await g.db_session.close()
                del g.db_session

    return wrapper


async def delete_item(
    session: AsyncSession,
    model_crud,
    id: int,
    redirect_endpoint: str,
    redirect_id: int | None = None,
):
    item = await model_crud.get(id, session)
    if item:
        await model_crud.remove(item, session)
    return redirect(url_for(redirect_endpoint, id=redirect_id))


def generate_password():
    length = 4
    password = "".join(random.choice(string.digits) for _ in range(length))
    return password


async def send_password_to_user(telegram_chat_id, password):
    await bot.send_message(
        telegram_chat_id,
        f"Ваш пароль для входа в админку: {password}",
    )


def nl2br(value: str) -> str:
    value = re.sub(r"\n\n", "</p><p>", value)
    value = value.replace("\n", "<br>")
    return f"<p>{value}</p>"
