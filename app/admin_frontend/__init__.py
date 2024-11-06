from quart import Quart
from .config import Config

app = Quart(__name__, static_folder='app/admin_frontend/static', static_url_path='/static')
app.config.from_object(Config)

from . import views  # noqa
