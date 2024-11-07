from functools import wraps

from quart import g
import requests

from core.db import AsyncSessionLocal
from core.settings import settings


BOT_TOKEN = settings.bot_token


def get_file_url(file_id: str) -> str:
    """Функция для получения URL изображения по file_id"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    result = response.json()
    if result["ok"]:
        file_path = result["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    return None


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
