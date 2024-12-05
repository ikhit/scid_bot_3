from quart import flash, redirect, render_template, url_for
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import get_image_url, send_image_to_telegram
from admin_frontend.forms import (
    MediaForm,
    QuestionForm,
    TextForm,
    URLForm,
    UserForm,
)
from crud import category_product_crud, info_crud, user_crud


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


async def add_question_form(
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


async def handle_user_form(session: AsyncSession, id: int | None = None):
    form = await UserForm().create_form()
    if id:
        user = await user_crud.get(id, session)
        if not form.is_submitted:
            form.telegram_id.data = user.tg_id
            form.name.data = user.name
            form.role.data = user.role
    if await form.validate_on_submit():
        if id:
            try:
                await user_crud.update(
                    user, form.role.data, session, form.name.data
                )
                return redirect(url_for(".get_user", id=user.id))
            except Exception as e:
                print(e)
        else:
            data = {
                "name": form.name.data,
                "tg_id": form.telegram_id.data,
                "role": form.role.data,
            }
            if await user_crud.get_user_by_tg_id(
                form.telegram_id.data, session
            ):
                await flash(
                    "Пользователь с таким Telegram ID уже существует",
                    category="error",
                )
                return redirect(url_for(".add_user"))
            try:
                user = await user_crud.create(data, session)
                return redirect(url_for(".get_user", id=user.id))
            except Exception as e:
                print(e)
    return await render_template("add_user.html", form=form)
