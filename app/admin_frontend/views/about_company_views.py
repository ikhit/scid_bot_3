from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    add_url_form,
    db_session,
    delete_item,
    update_url_form,
)
from crud import company_info_crud

about_company = Blueprint("about_company", __name__)

@about_company.route("/")
@db_session
async def get_company_about(session: AsyncSession):
    infos = await company_info_crud.get_multi(session)
    return await render_template(
        "list.html",
        data_list=infos,
        details_url=".get_company_about_details",
        title="Информация о компании",
        add_url=".add_info",
    )


@about_company.route("/<int:id>")
@db_session
async def get_company_about_details(session: AsyncSession, id: int):
    info = await company_info_crud.get(id, session)
    return await render_template(
        "detail.html",
        item=info,
        delete_url=".delete_about_company",
        update_url=".update_about_company",
    )


@about_company.route("/add", methods=["GET", "POST"])
@db_session
async def add_info(session: AsyncSession):
    return await add_url_form(
        session, company_info_crud, ".get_company_about_details"
    )


@about_company.route("/<int:id>/delete")
@db_session
async def delete_about_company(session: AsyncSession, id: int):
    return await delete_item(
        session, company_info_crud, id, ".get_company_about"
    )


@about_company.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_about_company(session: AsyncSession, id: int):
    return await update_url_form(
        session, company_info_crud, id, ".get_company_about_details"
    )
