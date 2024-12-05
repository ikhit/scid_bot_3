from sqlalchemy.ext.asyncio import AsyncSession
from quart import (
    redirect,
    render_template,
    session as q_session,
    url_for,
    Blueprint,
)
from redis_db.connect import get_redis_connection

from admin_frontend.forms import SetTimer
from admin_frontend.pagination import get_paginated_data_and_render
from admin_frontend.utils import db_session
from crud import feedback_crud, user_crud

from crud.request_to_manager import (
    close_case,
    get_all_manager_requests,
    get_all_support_requests,
    get_closed_cases,
    get_request,
)


managers = Blueprint("managers", __name__)


@managers.route("/")
@db_session
async def get_managers(session):
    users = await user_crud.get_multi(session)
    return await get_paginated_data_and_render(
        users,
        "managers.html",
        "Список администраторов",
        ".get_managers",
    )


@managers.route("/callbacks")
@db_session
async def get_manager_callbacks(session: AsyncSession):
    callbacks = await get_all_manager_requests(session)
    return await get_paginated_data_and_render(
        callbacks,
        "callbacks.html",
        "Заявки на обратный звонок",
        ".get_manager_callbacks",
    )


@managers.route("/support")
@db_session
async def get_support_requests(session: AsyncSession):
    callbacks = await get_all_support_requests(session)
    return await get_paginated_data_and_render(
        callbacks,
        "callbacks.html",
        "Заявки на техподдержку",
        ".get_support_requests",
    )


@managers.route("/closed-cases")
@db_session
async def get_all_closed_cases(session: AsyncSession):
    closed_cases = await get_closed_cases(session)
    return await get_paginated_data_and_render(
        closed_cases,
        "cases.html",
        "Закрытые заявки",
        ".get_all_closed_cases",
    )


@managers.route("/feedbacks")
@db_session
async def get_feedbacks(session: AsyncSession):
    feedbacks = await feedback_crud.get_multi(session)
    return await get_paginated_data_and_render(
        feedbacks,
        "feedbacks.html",
        "Отзывы",
        ".get_feedbacks",
    )


@managers.route("/specials", methods=["GET", "POST"])
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
        return redirect(url_for(".get_specials"))
    return await render_template("bot_data/specials.html", timer=timer, form=form)


@managers.route("/feedbacks/<int:id>")
@db_session
async def get_feedback(session: AsyncSession, id: int):
    feedback = await feedback_crud.get(id, session)
    return await render_template("feedback_card.html", feedback=feedback)


@managers.route("/case/<int:id>")
@db_session
async def close_current_case(session: AsyncSession, id: int):
    await close_case(q_session["user_id"], id, session)
    case = await get_request(id, session)
    url = (
        ".get_manager_callbacks"
        if case.need_contact_with_manager
        else ".get_support_requests"
    )
    return redirect(url_for(url))
