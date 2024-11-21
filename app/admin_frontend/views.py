from sqlalchemy.ext.asyncio import AsyncSession
from quart import render_template

from . import app
from crud import (
    products_crud,
    category_product_crud,
    portfolio_crud,
    info_crud,
    company_info_crud,
    user_crud,
    feedback_crud,
)
from models.models import QuestionEnum
from .utils import (
    add_text_form,
    add_url_form,
    delete_item,
    get_image_url,
    db_session,
)


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
        title="Список продуктов и услуг",
        add_url="add_product",
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
            data.media = get_image_url(data.media)
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
        title="Список дополнительных проектов",
        add_url="add_project",
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
        "list.html",
        data_list=questions,
        details_url="get_question_details",
        title="Общие вопросы",
        add_url="add_project",
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
        "list.html",
        data_list=questions,
        details_url="get_product_problems_details",
        title="Проблемы с продуктами",
        add_url="add_project",
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
        "list.html",
        data_list=infos,
        details_url="get_company_about_details",
        title="Информация о компании",
        add_url="add_info",
    )


@app.route("/about-company/<int:id>")
@db_session
async def get_company_about_details(session: AsyncSession, id: int):
    info = await company_info_crud.get(id, session)
    return await render_template("detail.html", item=info)


@app.route("/managers")
@db_session
async def get_managers(session):
    administration = await user_crud.get_manager_and_admin_list(session)
    return await render_template(
        "managers.html",
        data_list=administration,
        title="Список администраторов",
    )


@app.route("/feedbacks")
@db_session
async def get_feedbacks(session: AsyncSession):
    feedbacks = await feedback_crud.get_multi(session)
    return await render_template("feedbacks.html", data_list=feedbacks)


@app.route("/specials")
async def get_specials(): ...


@app.route("/add-project", methods=["GET", "POST"])
@db_session
async def add_project(session: AsyncSession):
    return await add_url_form(session, portfolio_crud, "get_project_details")


@app.route("/add-info", methods=["GET", "POST"])
@db_session
async def add_info(session: AsyncSession):
    return await add_url_form(session, info_crud, "get_company_about_details")


@app.route("/add-product", methods=["GET", "POST"])
@db_session
async def add_product(session: AsyncSession):
    return await add_text_form(session, products_crud, "get_product_details")


@app.route("/add-question", methods=["GET", "POST"])
@db_session
async def add_question(session: AsyncSession):
    return await add_text_form(session, info_crud, "get_question_details")


@app.route("/product-delete/<int:id>")
@db_session
async def delete_product(session: AsyncSession, id: int):
    return await delete_item(session, products_crud, id, "get_products")


@app.route("/question-delete/<int:id>")
@db_session
async def delete_question(session: AsyncSession, id: int):
    return await delete_item(session, info_crud, id, "get_questions")


@app.route("/question-delete/<int:id>")
@db_session
async def delete_about_combapy(session: AsyncSession, id: int):
    return await delete_item(
        session, company_info_crud, id, "get_company_about"
    )
