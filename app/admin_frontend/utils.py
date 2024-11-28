from functools import wraps
from io import BytesIO
import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from quart import g, redirect, url_for, render_template, flash
import requests

from admin_frontend.forms import (
    MediaForm,
    QuestionForm,
    TextForm,
    URLForm,
    UserForm,
)
from core.db import AsyncSessionLocal
from core.settings import settings
from core.bot_setup import bot
from crud import category_product_crud, info_crud, user_crud


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
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
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
            return redirect(
                url_for(details_url, id=details_id if details_id else item.id)
            )
        except Exception as e:
            print(e)
    return await render_template(
        "add_description.html",
        form=form,
    )


async def update_url_form(
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
):
    form = await URLForm().create_form()
    item = await model_crud.get(id, session)
    if not form.is_submitted:
        form.name.data = item.name
        form.url.data = item.url
    if await form.validate_on_submit():
        data = {
            "name": form.name.data,
            "url": form.url.data,
        }
        try:
            item = await model_crud.update(item, data, session)
            return redirect(
                url_for(details_url, id=details_id if details_id else item.id)
            )
        except Exception as e:
            print(e)
    return await render_template(
        "add_url.html",
        form=form,
    )


async def update_media_form(
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
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
            return redirect(
                url_for(details_url, id=details_id if details_id else item.id)
            )
        except Exception as e:
            print(e)
    return await render_template(
        "add_media.html",
        form=form,
        image=image,
    )


async def update_questions_form(
    session: AsyncSession,
    id: str,
    details_url: str,
):
    form = await QuestionForm().create_form()
    item = await info_crud.get(id, session)
    if not form.is_submitted:
        form.question.data = item.question
        form.answer.data = item.answer
    if await form.validate_on_submit():
        data = {
            "question": form.question.data,
            "answer": form.answer.data,
        }
        try:
            item = await info_crud.update(item, data, session)
            return redirect(url_for(details_url, id=item.id))
        except Exception as e:
            print(e)
    return await render_template(
        "add_question.html",
        form=form,
    )


async def edit_user_form(session: AsyncSession, id: int):
    form = await UserForm().create_form()
    user = await user_crud.get(id, session)
    if not form.is_submitted:
        form.telegram_id.data = user.tg_id
        form.name.data = user.name
        form.role.data = user.role
    if await form.validate_on_submit():
        try:
            await user_crud.update(user, form.role.data, session, form.name.data)
            return redirect(url_for("get_user", id=user.id))
        except Exception as e:
            print(e)
    return await render_template("add_user.html", form=form)


async def user_form(session: AsyncSession):
    form = await UserForm().create_form()
    if await form.validate_on_submit():
        data = {
            "name": form.name.data,
            "tg_id": form.telegram_id.data,
            "role": form.role.data,
        }
        if await user_crud.get_user_by_tg_id(form.telegram_id.data, session):
            await flash("Пользователь с таким Telegram ID уже существует", category="error")
            return redirect(url_for("add_user"))
        try:
            user = await user_crud.create(data, session)
            return redirect(url_for("get_user", id=user.id))
        except Exception as e:
            print(e)
    return await render_template("add_user.html", form=form)