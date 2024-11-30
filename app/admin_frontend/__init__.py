from quart import (
    Quart,
    redirect,
    render_template,
    session as q_session,
    url_for,
    request,
)
from quart_session import Session

from .utils import nl2br
from .config import Config
from .views import (
    about_company,
    auth,
    managers,
    products,
    projects,
    questions,
    users,
)

app = Quart(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)
app.config["SESSION_TYPE"] = "redis"
app.jinja_env.filters["nl2br"] = nl2br
app.register_blueprint(about_company, url_prefix="/about_company")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(products, url_prefix="/products")
app.register_blueprint(managers, url_prefix="/managers")
app.register_blueprint(projects, url_prefix="/projects")
app.register_blueprint(questions, url_prefix="/questions")
app.register_blueprint(users, url_prefix="/users")

Session(app)


@app.before_request
async def check_authorization():
    if "user_id" not in q_session and request.endpoint not in [
        "admin_login",
        "admin_password",
    ]:
        return redirect(url_for("admin_login"))


@app.route("/")
async def index():
    return await render_template("base.html")
