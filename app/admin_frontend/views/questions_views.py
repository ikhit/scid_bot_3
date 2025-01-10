from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    db_session,
    delete_item,
)
from admin_frontend.form_handlers import (
    add_question_form,
    update_questions_form,
)
from admin_frontend.pagination import get_paginated_data_and_render
from crud import info_crud
from models.models import QuestionEnum

questions = Blueprint("questions", __name__)


@questions.route("/")
@db_session
async def get_questions(session: AsyncSession):
    questions = await info_crud.get_all_questions_by_type(
        QuestionEnum.GENERAL_QUESTIONS, session
    )
    return await get_paginated_data_and_render(
        data=questions,
        template_name="bot_data/list.html",
        title="Общие вопросы",
        endpoint=".get_questions",
        details_url=".get_question_details",
        add_url=".add_question",
    )


@questions.route("/<int:id>")
@db_session
async def get_question_details(session: AsyncSession, id: int):
    question = await info_crud.get(id, session)
    return await render_template(
        "bot_data/card.html",
        item=question,
        delete_url=".delete_question",
        update_url=".update_question",
    )


@questions.route("/problems")
@db_session
async def get_product_problems(session: AsyncSession):
    questions = await info_crud.get_all_questions_by_type(
        QuestionEnum.PROBLEMS_WITH_PRODUCTS, session
    )
    return await get_paginated_data_and_render(
        data=questions,
        template_name="bot_data/list.html",
        title="Проблемы с продуктами",
        endpoint=".get_questions",
        details_url=".get_question_details",
        add_url=".add_problems_with_product",
    )


@questions.route("/add", methods=["GET", "POST"])
@db_session
async def add_question(session: AsyncSession):
    return await add_question_form(
        session,
        QuestionEnum.GENERAL_QUESTIONS,
        ".get_question_details",
    )


@questions.route("/problems/add", methods=["GET", "POST"])
@db_session
async def add_problems_with_product(session: AsyncSession):
    return await add_question_form(
        session,
        QuestionEnum.PROBLEMS_WITH_PRODUCTS,
        ".get_question_details",
    )


@questions.route("/<int:id>/delete")
@db_session
async def delete_question(session: AsyncSession, id: int):
    return await delete_item(session, info_crud, id, ".get_questions")


@questions.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_question(session: AsyncSession, id: int):
    return await update_questions_form(session, id, ".get_question_details")
