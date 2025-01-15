from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    db_session,
    delete_item,
)
from admin_frontend.form_handlers import add_url_form, update_url_form
from admin_frontend.pagination import get_paginated_data_and_render
from crud import portfolio_crud

projects = Blueprint("projects", __name__)


@projects.route("/<int:id>")
@db_session
async def get_project_details(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на отображение подробной информации о проекте.
    Функция извлекает проект по заданному ID и отображает его детали. 
    Также предоставляет ссылки для обновления и удаления проекта.
    """
    project = await portfolio_crud.get(id, session)
    return await render_template(
        "bot_data/card.html",
        item=project,
        delete_url=".delete_project",
        update_url=".update_project",
    )


@projects.route("/")
@db_session
async def get_projects(session: AsyncSession):
    """
    Обрабатывает запрос на получение списка всех проектов.
    Функция извлекает все проекты из базы данных и отображает их на странице
    с пагинацией. Также предоставляет возможность добавления нового проекта.
    """
    projects = await portfolio_crud.get_multi(session)
    return await get_paginated_data_and_render(
        data=projects,
        template_name="bot_data/list.html",
        title="Список дополнительных проектов",
        endpoint=".get_projects",
        details_url=".get_project_details",
        add_url=".add_project",
    )


@projects.route("/add", methods=["GET", "POST"])
@db_session
async def add_project(session: AsyncSession):
    """
    Обрабатывает запрос на добавление нового проекта.
    Если запрос GET, отображается форма для добавления нового проекта.
    Если запрос POST, форма отправляется для обработки.
    """
    return await add_url_form(session, portfolio_crud, ".get_project_details")


@projects.route("/<int:id>/delete")
@db_session
async def delete_project(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на удаление проекта.
    Функция удаляет проект по заданному ID из базы данных и перенаправляет 
    на страницу с проектами.
    """
    return await delete_item(
        session, portfolio_crud, id, ".get_project_details"
    )


@projects.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_project(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на обновление информации о проекте.
    Если запрос GET, отображается форма для обновления информации о проекте.
    Если запрос POST, форма отправляется для обработки.
    """
    return await update_url_form(
        session, portfolio_crud, id, ".get_project_details"
    )
