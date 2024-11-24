from functools import wraps
from io import BytesIO

from sqlalchemy.ext.asyncio import AsyncSession
from quart import g, redirect, url_for, render_template
import requests

from admin_frontend.forms import MediaForm, QuestionForm, TextForm, URLForm
from core.db import AsyncSessionLocal
from core.settings import settings
from crud import category_product_crud, info_crud


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


async def add_product_media_form(
    session: AsyncSession, details_url: str, product_id: int
):
    form = await MediaForm().create_form()
    if await form.validate_on_submit():
        image_data = form.media.data.read()
        media = send_image_to_telegram(image_data)
        info_data = {
            "name": form.name.data,
            "media": media,
            "description": form.description.data,
            "product_id": product_id,
        }
        try:
            await category_product_crud.create(info_data, session)
            return redirect(url_for(details_url, id=product_id))
        except Exception as e:
            print(e)
    return await render_template("add_media.html", form=form)


async def add_product_url_form(
    session: AsyncSession, details_url: str, product_id: int
):
    form = await URLForm().create_form()
    if await form.validate_on_submit():
        info_data = {
            "name": form.name.data,
            "url": form.url.data,
            "product_id": product_id,
        }
        try:
            await category_product_crud.create(info_data, session)
            return redirect(url_for(details_url, id=product_id))
        except Exception as e:
            print(e)
    return await render_template("add_url.html", form=form)


async def add_product_text_form(
    session: AsyncSession, details_url: str, product_id: int
):
    form = await TextForm().create_form()
    if await form.validate_on_submit():
        info_data = {
            "name": form.name.data,
            "description": form.description.data,
            "product_id": product_id,
        }
        try:
            await category_product_crud.create(info_data, session)
            return redirect(url_for(details_url, id=product_id))
        except Exception as e:
            print(e)
    return await render_template("add_description.html", form=form)


async def add_questions(
    session: AsyncSession, question_category: str, details_url: str
):
    form = await QuestionForm().create_form()
    if await form.validate_on_submit():
        data = {
            "question": form.question.data,
            "answer": form.answer.data,
            "question_type": question_category,
        }
        try:
            item = await info_crud.create(data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_question.html",
        form=form,
    )


async def update_text_form(
    session: AsyncSession, model_crud, id: str, details_url: str
):
    form = await TextForm().create_form()
    item = await model_crud.get(id, session)
    if not form.is_submitted:
        form.name.data = item.name
        form.description.data = item.description
    if await form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data,
        }
        try:
            item = await model_crud.update(item, data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_description.html",
        form=form,
    )


async def update_url_form(
    session: AsyncSession, model_crud, id: str, details_url: str
):
    form = await URLForm().create_form()
    item = await model_crud.get(id, session)
    if not form.is_submitted:
        form.name.data = item.name
        form.url.data = item.url
    if await form.validate_on_submit():
        data = {
            "name": form.name.data,
            "url": form.description.data,
        }
        try:
            item = await model_crud.update(item, data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_url.html",
        form=form,
    )


async def update_media_form(
    session: AsyncSession, model_crud, id: str, details_url: str
):
    form = await MediaForm().create_form()
    item = await model_crud.get(id, session)
    if not form.is_submitted:
        form.name.data = item.name
        image = get_image_url(item.media)
    if await form.validate_on_submit():
        image_data = form.media.data.read()
        media = send_image_to_telegram(image_data)
        data = {
            "name": form.name.data,
            "media": media,
        }
        try:
            item = await model_crud.update(item, data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_media.html",
        form=form,
        image=image,
    )
