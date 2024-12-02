from sqlalchemy.ext.asyncio import AsyncSession
from quart import (
    redirect,
    render_template,
    request,
    session as q_session,
    url_for,
    Blueprint,
)
from redis_db.connect import get_redis_connection

from admin_frontend.forms import SetTimer
from admin_frontend.utils import db_session, paginate_objects
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
    administration = await user_crud.get_manager_and_admin_list(session)
    return await render_template(
        "managers.html",
        data_list=administration,
        title="Список администраторов",
    )


@managers.route("/callbacks")
@db_session
async def get_manager_callbacks(session: AsyncSession):
    callbacks = await get_all_manager_requests(session)
    return await render_template(
        "callbacks.html",
        data_list=callbacks,
        title="Заявки на обратный звонок",
    )


@managers.route("/support")
@db_session
async def get_support_requests(session: AsyncSession):
    callbacks = await get_all_support_requests(session)
    return await render_template(
        "callbacks.html", data_list=callbacks, title="Заявки на техподдержку"
    )


@managers.route("/closed-cases")
@db_session
async def get_all_closed_cases(session: AsyncSession):
    closed_cases = await get_closed_cases(session)
    return await render_template(
        "cases.html", data_list=closed_cases, title="Закрытые заявки"
    )


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


@managers.route("/feedbacks")
@db_session
async def get_feedbacks(session: AsyncSession):
    page = request.args.get("page", 1, type=int)
    feedbacks = await feedback_crud.get_multi(session)
    paginated_feedbacks, total_pages = paginate_objects(
        feedbacks, page=page, per_page=5
    )

    return await render_template(
        "feedbacks.html",
        data_list=paginated_feedbacks,
        title="Список отзывов от пользователей",
        current_page=page,
        total_pages=total_pages,
        endpoint=".get_feedbacks",
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
    return await render_template("specials.html", timer=timer, form=form)


@managers.route("/feedbacks/<int:id>")
@db_session
async def get_feedback(session: AsyncSession, id: int):
    feedback = await feedback_crud.get(id, session)
    return await render_template("feedback_text.html", feedback=feedback)
