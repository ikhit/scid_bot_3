from sqlalchemy.ext.asyncio import AsyncSession
from quart import render_template

from . import app
from crud import (
    products_crud,
    category_product_crud,
    portfolio_crud,
    info_crud,
    company_info_crud,
)
from models.models import QuestionEnum
from .utils import get_file_url, db_session


@app.route("/", methods=["GET"])
async def index():
    return await render_template("base.html")


@app.route("/products")
@db_session
async def get_products(session: AsyncSession):
    """Вывести список всех продуктов."""
    products = await products_crud.get_multi(session)
    return await render_template(
        "list.html",
        data_list=products,
        details_url="get_product_details",
    )


@app.route("/products/<int:id>", methods=["GET"])
@db_session
async def get_product_details(session: AsyncSession, id: int):
    """Вывести всю информацию о продукте."""
    product_data = await category_product_crud.get_category_by_product_id(
        id, session
    )
    product = await products_crud.get(id, session)
    for data in product_data:
        if data.media:
            data.media = get_file_url(data.media)
    return await render_template(
        "detail.html", item=product, item_data=product_data
    )


@app.route("/projects")
@db_session
async def get_projects(session: AsyncSession):
    projects = await portfolio_crud.get_multi(session)
    return await render_template(
        "list.html",
        data_list=projects,
        details_url="get_project_details",
    )


@app.route("/projects/<int:id>")
@db_session
async def get_project_details(session: AsyncSession, id: int):
    project = await portfolio_crud.get(id, session)
    return await render_template("detail.html", item=project)


@app.route("/questions")
@db_session
async def get_questions(session: AsyncSession):
    questions = await info_crud.get_all_questions_by_type(
        QuestionEnum.GENERAL_QUESTIONS, session
    )
    return await render_template(
        "list.html", data_list=questions, details_url="get_question_details"
    )


@app.route("/questions/<int:id>")
@db_session
async def get_question_details(session: AsyncSession, id: int):
    question = await info_crud.get(id, session)
    return await render_template("detail.html", item=question)


@app.route("/problems")
@db_session
async def get_product_problems(session: AsyncSession):
    questions = await info_crud.get_all_questions_by_type(
        QuestionEnum.PROBLEMS_WITH_PRODUCTS, session
    )
    return await render_template(
        "list.html", data_list=questions, details_url="get_product_problems_details"
    )


@app.route("/problems/<int:id>")
@db_session
async def get_product_problems_details(session: AsyncSession, id: int):
    question = await info_crud.get(id, session)
    return await render_template("detail.html", item=question)

@app.route("/about-company")
@db_session
async def get_company_about(session: AsyncSession):
    infos = await company_info_crud.get_multi(session)
    return await render_template(
        "list.html", data_list=infos, details_url="get_company_about_details"
    )


@app.route("/about-company/<int:id>")
@db_session
async def get_company_about_details(session: AsyncSession, id: int):
    info = await company_info_crud.get(id, session)
    return await render_template("detail.html", item=info)
