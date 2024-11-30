from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    add_url_form,
    db_session,
    delete_item,
    update_url_form,
)
from crud import portfolio_crud

projects = Blueprint("projects", __name__)


@projects.route("/<int:id>")
@db_session
async def get_project_details(session: AsyncSession, id: int):
    project = await portfolio_crud.get(id, session)
    return await render_template(
        "detail.html",
        item=project,
        delete_url=".delete_project",
        update_url=".update_project",
    )


@projects.route("/")
@db_session
async def get_projects(session: AsyncSession):
    projects = await portfolio_crud.get_multi(session)
    return await render_template(
        "list.html",
        data_list=projects,
        details_url=".get_project_details",
        title="Список дополнительных проектов",
        add_url=".add_project",
    )


@projects.route("/add", methods=["GET", "POST"])
@db_session
async def add_project(session: AsyncSession):
    return await add_url_form(session, portfolio_crud, ".get_project_details")


@projects.route("/<int:id>/delete")
@db_session
async def delete_project(session: AsyncSession, id: int):
    return await delete_item(
        session, portfolio_crud, id, ".get_project_details"
    )


@projects.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_project(session: AsyncSession, id: int):
    return await update_url_form(
        session, portfolio_crud, id, ".get_project_details"
    )
