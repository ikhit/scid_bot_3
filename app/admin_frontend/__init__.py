import re

from quart import Quart

from .config import Config

app = Quart(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

def nl2br(value):
        # Заменяем два символа новой строки (для абзаца) на закрытие и открытие <p>
    value = re.sub(r'\n\n', '</p><p>', value)
    # Заменяем один символ новой строки на <br>
    value = value.replace('\n', '<br>')
    # Добавляем <p> в начало и конец, чтобы весь текст был в абзацах
    return f'<p>{value}</p>'

app.jinja_env.filters['nl2br'] = nl2br

from . import views  # noqa
