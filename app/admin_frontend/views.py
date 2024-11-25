from sqlalchemy.ext.asyncio import AsyncSession
from quart import render_template, redirect, url_for

from admin_frontend.forms import SetTimer
from redis_db.connect import get_redis_connection
from crud.request_to_manager import (
    get_all_manager_requests,
    get_all_support_requests,
    get_closed_cases,
)

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
    add_product_media_form,
    add_product_text_form,
    add_product_url_form,
    add_questions,
    add_text_form,
    add_url_form,
    delete_item,
    get_image_url,
    db_session,
    update_media_form,
    update_questions_form,
    update_text_form,
    update_url_form,
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
        "bot_data/product_details.html",
        item=product,
        item_data=product_data,
        delete_url="delete_product",
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
    return await render_template(
        "detail.html",
        item=project,
        delete_url="delete_project",
        update_url="update_project",
    )


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
        add_url="add_question",
    )


@app.route("/questions/<int:id>")
@db_session
async def get_question_details(session: AsyncSession, id: int):
    question = await info_crud.get(id, session)
    return await render_template(
        "detail.html",
        item=question,
        delete_url="delete_question",
        update_url="update_question",
    )


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
        add_url="add_problems_with_product",
    )


@app.route("/problems/<int:id>")
@db_session
async def get_product_problems_details(session: AsyncSession, id: int):
    question = await info_crud.get(id, session)
    return await render_template(
        "detail.html",
        item=question,
        delete_url="delete_question",
        update_url="update_problems",
    )


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
    return await render_template(
        "detail.html",
        item=info,
        delete_url="delete_about_company",
        update_url="update_about_company",
    )


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


@app.route("/specials", methods=["GET", "POST"])
async def get_specials():
    redis_client = await get_redis_connection()
    timer = await redis_client.get("timeout")
    await redis_client.close()
    form = await SetTimer().create_form()
    if await form.validate_on_submit():
        try:
            await redis_client.set("timeout", form.timer.data)
            await redis_client.close()
        except Exception as e:
            print(e)
        return redirect(url_for("get_specials"))
    return await render_template("specials.html", timer=timer, form=form)


@app.route("/add-project", methods=["GET", "POST"])
@db_session
async def add_project(session: AsyncSession):
    return await add_url_form(session, portfolio_crud, "get_project_details")


@app.route("/add-about-company", methods=["GET", "POST"])
@db_session
async def add_info(session: AsyncSession):
    return await add_url_form(
        session, company_info_crud, "get_company_about_details"
    )


@app.route("/add-product", methods=["GET", "POST"])
@db_session
async def add_product(session: AsyncSession):
    return await add_text_form(session, products_crud, "get_product_details")


@app.route("/add-question", methods=["GET", "POST"])
@db_session
async def add_question(session: AsyncSession):
    return await add_questions(
        session,
        QuestionEnum.GENERAL_QUESTIONS,
        "get_question_details",
    )


@app.route("/add-problems", methods=["GET", "POST"])
@db_session
async def add_problems_with_product(session: AsyncSession):
    return await add_questions(
        session,
        QuestionEnum.PROBLEMS_WITH_PRODUCTS,
        "get_question_details",
    )


@app.route("/products/<int:id>/delete")
@db_session
async def delete_product(session: AsyncSession, id: int):
    return await delete_item(session, products_crud, id, "get_products")


@app.route("/products/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_product(session: AsyncSession, id: int):
    return await update_text_form(
        session, products_crud, id, "get_product_details"
    )


@app.route("/projects/<int:id>/delete")
@db_session
async def delete_project(session: AsyncSession, id: int):
    return await delete_item(
        session, portfolio_crud, id, "get_project_details"
    )


@app.route("/questions/<int:id>/delete")
@db_session
async def delete_question(session: AsyncSession, id: int):
    return await delete_item(session, info_crud, id, "get_questions")


@app.route("/about-company/<int:id>/delete")
@db_session
async def delete_about_company(session: AsyncSession, id: int):
    return await delete_item(
        session, company_info_crud, id, "get_company_about"
    )


@app.route("/products/<int:id>/add-media", methods=["GET", "POST"])
@db_session
async def add_product_media(session: AsyncSession, id: int):
    return await add_product_media_form(session, "get_product_details", id)


@app.route("/products/<int:id>/add-url", methods=["GET", "POST"])
@db_session
async def add_product_url(session: AsyncSession, id: int):
    return await add_product_url_form(session, "get_product_details", id)


@app.route("/products/<int:id>/add-text", methods=["GET", "POST"])
@db_session
async def add_product_text(session: AsyncSession, id: int):
    return await add_product_text_form(session, "get_product_details", id)


@app.route("/manager-callbacks")
@db_session
async def get_manager_callbacks(session: AsyncSession):
    callbacks = await get_all_manager_requests(session)
    return await render_template(
        "callbacks.html",
        data_list=callbacks,
        title="Заявки на обратный звонок",
    )


@app.route("/support-callbacks")
@db_session
async def get_support_requests(session: AsyncSession):
    callbacks = await get_all_support_requests(session)
    return await render_template(
        "callbacks.html", data_list=callbacks, title="Заявки на техподдержку"
    )


@app.route("/closed-cases")
@db_session
async def get_all_closed_cases(session: AsyncSession):
    closed_cases = await get_closed_cases(session)
    return await render_template(
        "cases.html", data_list=closed_cases, title="Закрытые заявки"
    )


@app.route("/update-category/<int:id>", methods=["GET", "POST"])
@db_session
async def update_category(session: AsyncSession, id: int):
    category = await category_product_crud.get(id, session)
    if category.url:
        return await update_url_form(
            session,
            category_product_crud,
            id,
            "get_product_details",
            category.product_id,
        )
    if not category.media:
        return await update_text_form(
            session,
            category_product_crud,
            id,
            "get_product_details",
            category.product_id,
        )
    else:
        return await update_media_form(
            session,
            category_product_crud,
            id,
            "get_product_details",
            category.product_id,
        )


@app.route("/delete-category/<int:id>", methods=["GET", "POST"])
@db_session
async def delete_category(session: AsyncSession, id: int):
    category = await category_product_crud.get(id, session)
    return await delete_item(
        session,
        category_product_crud,
        id,
        "get_product_details",
        category.product_id,
    )


@app.route("/update-about-company/<int:id>", methods=["GET", "POST"])
@db_session
async def update_about_company(session: AsyncSession, id: int):
    return await update_url_form(
        session, company_info_crud, id, "get_company_about_details"
    )


@app.route("/update-project/<int:id>", methods=["GET", "POST"])
@db_session
async def update_project(session: AsyncSession, id: int):
    return await update_url_form(
        session, portfolio_crud, id, "get_project_details"
    )


@app.route("/upate-question/<int:id>", methods=["GET", "POST"])
@db_session
async def update_question(session: AsyncSession, id: int):
    return await update_questions_form(session, id, "get_question_details")


@app.route("/upate-problems/<int:id>", methods=["GET", "POST"])
@db_session
async def update_problems(session: AsyncSession, id: int):
    return await update_questions_form(
        session, id, "add_problems_with_product"
    )
