import re

from quart import Quart
from quart_session import Session

from .config import Config

app = Quart(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)
session = Session(app)


def nl2br(value):
    value = re.sub(r"\n\n", "</p><p>", value)
    value = value.replace("\n", "<br>")
    return f"<p>{value}</p>"


app.jinja_env.filters["nl2br"] = nl2br

from . import views  # noqa
