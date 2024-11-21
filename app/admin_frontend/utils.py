from functools import wraps
from io import BytesIO

from sqlalchemy.ext.asyncio import AsyncSession
from quart import g, redirect, url_for, render_template
import requests

from admin_frontend.forms import TextForm, URLForm
from core.db import AsyncSessionLocal
from core.settings import settings


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
    """
    url = f"https://api.telegram.org/bot{settings.bot_token}/sendPhoto"
    files = {"photo": ("image.jpg", BytesIO(image_data), "image/jpeg")}
    data = {"chat_id": settings.telegram_chat_ids}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    if result["ok"]:
        return result["result"]["photo"][0]["file_id"]
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
    session: AsyncSession, model_crud, id: int, redirect_endpoint: str
):
    item = await model_crud.get(id, session)
    if item:
        await model_crud.remove(item, session)
    return redirect(url_for(redirect_endpoint))


async def add_text_form(session: AsyncSession, model_crud, details_url: str):
    form = await TextForm().create_form()
    if await form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data,
        }
        try:
            item = await model_crud.create(data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_description.html",
        form=form,
    )


async def add_url_form(
    session: AsyncSession,
    model_crud,
    details_url: str,
):
    form = await URLForm().create_form()
    if await form.validate_on_submit():
        info_data = {
            "name": form.name.data,
            "url": form.url.data,
        }
        try:
            item = await model_crud.create(info_data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template("add_url.html", form=form)
