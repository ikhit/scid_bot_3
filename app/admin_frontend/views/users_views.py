from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import db_session
from admin_frontend.form_handlers import handle_user_form
from crud import user_crud
from crud.request_to_manager import get_manager_stats

users = Blueprint("users", __name__)


@users.route("/<int:id>")
@db_session
async def get_user(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на отображение подробной информации о пользователе.
    Функция извлекает пользователя по заданному ID и отображает его данные. 
    Также показывает информацию о количестве закрытых случаев пользователя 
    и последний случай.
    """
    user = await user_crud.get(id, session)
    closed_cases, last_case = await get_manager_stats(user.tg_id, session)
    return await render_template(
        "bot_data/card.html",
        user=user,
        closed_cases=closed_cases,
        last_case=last_case,
    )


@users.route("/add", methods=["GET", "POST"])
@db_session
async def add_user(session: AsyncSession):
    """
    Обрабатывает запрос на добавление нового пользователя.
    Если запрос GET, отображается форма для добавления нового пользователя.
    Если запрос POST, форма отправляется для обработки.
    """
    return await handle_user_form(session)


@users.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_user(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на обновление информации о пользователе.
    Если запрос GET, отображается форма для обновления информации
    о пользователе. Если запрос POST, форма отправляется для обработки.
    """
    return await handle_user_form(session, id)
