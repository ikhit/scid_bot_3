from quart import Quart
from .config import Config

app = Quart(__name__)
app.config.from_object(Config)

from . import views  # noqa
