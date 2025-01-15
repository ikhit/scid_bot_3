from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    db_session,
    delete_item,
)
from admin_frontend.form_handlers import add_url_form, update_url_form
from admin_frontend.pagination import get_paginated_data_and_render
from crud import company_info_crud

about_company = Blueprint("about_company", __name__)


@about_company.route("/")
@db_session
async def get_company_about(session: AsyncSession):
    """
    Обрабатывает запрос на страницу с информацией о компании.
    Функция извлекает все записи о компании из базы данных,
    используя CRUD операции, и возвращает страницу с пагинацией,
    отображающую эти данные.
    """
    infos = await company_info_crud.get_multi(session)
    return await get_paginated_data_and_render(
        data=infos,
        template_name="bot_data/list.html",
        title="Информация о компании",
        endpoint=".get_company_about",
        add_url=".add_info",
        details_url=".get_company_about_details",
    )


@about_company.route("/<int:id>")
@db_session
async def get_company_about_details(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на отображение подробной информации о
    компании по ее ID. Функция извлекает одну запись о компании
    по заданному идентификатору и отображает
    ее на странице с использованием шаблона карточки.
    """
    info = await company_info_crud.get(id, session)
    return await render_template(
        "bot_data/card.html",
        item=info,
        delete_url=".delete_about_company",
        update_url=".update_about_company",
    )


@about_company.route("/add", methods=["GET", "POST"])
@db_session
async def add_info(session: AsyncSession):
    """
    Обрабатывает запрос на добавление новой информации о компании.
    Функция либо отображает форму для добавления новой информации о компании,
    либо обрабатывает отправку данных формы.
    """
    return await add_url_form(
        session, company_info_crud, ".get_company_about_details"
    )


@about_company.route("/<int:id>/delete")
@db_session
async def delete_about_company(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на удаление информации о компании по ее ID.
    Функция удаляет запись о компании из базы данных по указанному ID и
    перенаправляет пользователя на страницу с общим списком информации 
    о компании.
    """
    return await delete_item(
        session, company_info_crud, id, ".get_company_about"
    )


@about_company.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_about_company(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на обновление информации о компании по ее ID.
    Функция либо отображает форму для обновления информации о 
    компании по заданному ID, либо обрабатывает отправку обновленных 
    данных формы.
    """
    return await update_url_form(
        session, company_info_crud, id, ".get_company_about_details"
    )
