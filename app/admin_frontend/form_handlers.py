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
    """
    Обрабатывает форму для добавления нового текста.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param model_crud: Класс или объект с методами CRUD для работы с моделью.
    :param details_url: URL для перенаправления после успешного добавления.
    :return: Перенаправление на страницу с деталями объекта или отображение формы для добавления текста.
    """
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
        "bot_data/add_item_form.html", form=form, title="Добавить текст"
    )


async def update_text_form(
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
):
    """
    Обрабатывает форму для обновления текста.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param model_crud: Класс или объект с методами CRUD для работы с моделью.
    :param id: Идентификатор элемента, который нужно обновить.
    :param details_url: URL для перенаправления после успешного обновления.
    :param details_id: Идентификатор, используемый при формировании URL для перенаправления (по умолчанию None).
    :return: Перенаправление на страницу с деталями объекта или отображение формы для редактирования текста.
    """
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
        "bot_data/add_item_form.html", form=form, title="Отредактировать текст"
    )


async def add_url_form(
    session: AsyncSession,
    model_crud,
    details_url: str,
):
    """
    Обрабатывает форму для добавления новой ссылки.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param model_crud: Класс или объект с методами CRUD для работы с моделью.
    :param details_url: URL для перенаправления после успешного добавления.
    :return: Перенаправление на страницу с деталями объекта или отображение формы для добавления ссылки.
    """
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
    return await render_template(
        "bot_data/add_item_form.html", form=form, title="Добавить ссылку"
    )


async def update_url_form(
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
):
    """
    Обрабатывает форму для обновления ссылки.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param model_crud: Класс или объект с методами CRUD для работы с моделью.
    :param id: Идентификатор элемента, который нужно обновить.
    :param details_url: URL для перенаправления после успешного обновления.
    :param details_id: Идентификатор, используемый при формировании URL для перенаправления (по умолчанию None).
    :return: Перенаправление на страницу с деталями объекта или отображение формы для редактирования ссылки.
    """
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
        "bot_data/add_item_form.html",
        form=form,
        title="Отредактировать ссылку",
    )


async def add_question_form(
    session: AsyncSession, question_category: str, details_url: str
):
    """
    Обрабатывает форму для добавления нового вопроса.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param question_category: Категория вопроса.
    :param details_url: URL для перенаправления после успешного добавления.
    :return: Перенаправление на страницу с деталями объекта или отображение формы для добавления вопроса.
    """
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
        "bot_data/add_item_form.html", form=form, title="Добавить вопросы"
    )


async def update_questions_form(
    session: AsyncSession,
    id: str,
    details_url: str,
):
    """
    Обрабатывает форму для обновления вопроса.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param id: Идентификатор вопроса, который нужно обновить.
    :param details_url: URL для перенаправления после успешного обновления.
    :return: Перенаправление на страницу с деталями объекта или отображение формы для редактирования вопроса.
    """
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
        "bot_data/add_item_form.html",
        form=form,
        title="Отредактировать вопросы",
    )


async def add_product_url_form(
    session: AsyncSession, details_url: str, product_id: int
):
    """
    Обрабатывает форму для добавления ссылки к продукту.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param details_url: URL для перенаправления после успешного добавления.
    :param product_id: Идентификатор продукта, к которому добавляется ссылка.
    :return: Перенаправление на страницу с деталями продукта или отображение формы для добавления ссылки.
    """
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
    return await render_template(
        "bot_data/add_item_form.html",
        form=form,
        title="Добавить ссылку к дополению",
    )


async def add_product_text_form(
    session: AsyncSession, details_url: str, product_id: int
):
    """
    Обрабатывает форму для добавления текста к продукту.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param details_url: URL для перенаправления после успешного добавления.
    :param product_id: Идентификатор продукта, к которому добавляется текст.
    :return: Перенаправление на страницу с деталями продукта или отображение формы для добавления текста.
    """
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
    return await render_template(
        "bot_data/add_item_form.html",
        form=form,
        title="Добавить текст к дополнению",
    )


async def add_product_media_form(
    session: AsyncSession, details_url: str, product_id: int
):
    """
    Обрабатывает форму для добавления медиа-файла (например, изображения) к продукту.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param details_url: URL для перенаправления после успешного добавления.
    :param product_id: Идентификатор продукта, к которому добавляется медиа-файл.
    :return: Перенаправление на страницу с деталями продукта или отображение формы для добавления медиа.
    """
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
    return await render_template(
        "bot_data/add_item_form.html",
        form=form,
        title="Добавить картинку к дополнению",
    )


async def update_media_form(
    session: AsyncSession,
    model_crud,
    id: str,
    details_url: str,
    details_id: int | None = None,
):
    """
    Обрабатывает форму для обновления медиа-файла (например, изображения) у объекта.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param model_crud: Класс или объект с методами CRUD для работы с моделью.
    :param id: Идентификатор объекта, который нужно обновить.
    :param details_url: URL для перенаправления после успешного обновления.
    :param details_id: Идентификатор, используемый при формировании URL для перенаправления (по умолчанию None).
    :return: Перенаправление на страницу с деталями объекта или отображение формы для редактирования медиа.
    """
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
        "bot_data/add_item_form.html",
        form=form,
        image=image,
        title="Отредактировать картинку к дополнению",
    )


async def handle_user_form(session: AsyncSession, id: int | None = None):
    """
    Обрабатывает форму для добавления или обновления данных пользователя.

    :param session: Асинхронная сессия для взаимодействия с базой данных.
    :param id: Идентификатор пользователя для обновления (по умолчанию None для создания нового пользователя).
    :return: Перенаправление на страницу с деталями пользователя или отображение формы для добавления/редактирования пользователя.
    """
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
    return await render_template(
        "bot_data/add_item_form.html", form=form, title="Данные пользователя"
    )
