from quart import (
    redirect,
    render_template,
    request,
    session as q_session,
    url_for,
    Blueprint,
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from admin_frontend.utils import (
    db_session,
    generate_password,
    send_password_to_user,
)
from crud import user_crud
from models.models import RoleEnum
from redis_db.connect import get_redis_connection

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
@db_session
async def admin_login(db_session: AsyncSession):
    if request.method == "POST":
        form_data = await request.form
        if "telegram_id" not in form_data:
            return "Telegram ID не был передан"
        telegram_id = int(form_data["telegram_id"])
        user = await user_crud.get_user_by_tg_id(telegram_id, db_session)
        if user.role == RoleEnum.USER:
            return "У вас нет прав администратора"
        password = generate_password()
        redis_client = await get_redis_connection()
        await redis_client.setex(
            f"admin_password_{telegram_id}", timedelta(hours=24), password
        )
        await redis_client.close()
        await send_password_to_user(telegram_id, password)
        q_session["telegram_id"] = telegram_id
        return redirect(url_for(".admin_password"))

    return await render_template("auth/login.html")


@auth.route("/password", methods=["GET", "POST"])
async def admin_password():
    if request.method == "POST":
        telegram_id = q_session.get("telegram_id")
        if not telegram_id:
            return redirect(url_for(".admin_login"))
        form_data = await request.form
        entered_password = form_data["password"]
        redis_client = await get_redis_connection()
        stored_password = await redis_client.get(
            f"admin_password_{telegram_id}"
        )
        await redis_client.close()
        if stored_password is None:
            return "Пароль устарел или не найден, попробуйте снова через бота."
        if entered_password == stored_password:
            q_session["user_id"] = telegram_id
            return redirect(url_for("index"))
        return "Неверный пароль"

    return await render_template("auth/password.html")


@auth.route("/logout")
def logout():
    q_session.pop("user_id", None)
    return redirect(url_for(".admin_login"))
