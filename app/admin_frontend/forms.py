from quart_wtf import QuartForm, FileRequired
from wtforms import (
    StringField,
    SubmitField,
    URLField,
    TextAreaField,
    FileField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired, Optional

from .validators import validate_button_len
from models.models import RoleEnum


class BaseForm(QuartForm):
    name = StringField(
        "Введите название",
        validators=[
            DataRequired(message="Обязательное поле"),
            validate_button_len,
        ],
    )
    submit = SubmitField("Добавить")


class URLForm(BaseForm):
    url = URLField(
        "Добавьте ссылку",
        validators=[
            DataRequired(message="Обязательное поле"),
        ],
    )


class TextForm(BaseForm):
    description = TextAreaField(
        "Введите текст",
        validators=[
            DataRequired(message="Обязательное поле"),
        ],
    )


class MediaForm(BaseForm):
    media = FileField(
        validators=[
            FileRequired(),
        ]
    )
    description = TextAreaField(
        "Введите текст",
        validators=[
            Optional(),
        ],
    )


class QuestionForm(QuartForm):
    question = StringField(
        "Введите название категории вопросов",
        validators=[
            DataRequired(message="Обязательное поле"),
            validate_button_len,
        ],
    )
    answer = TextAreaField(
        "Введите список вопросов и ответов",
        validators=[
            DataRequired(message="Обязательное поле"),
        ],
    )
    submit = SubmitField("Добавить")


class SetTimer(QuartForm):
    timer = IntegerField(
        "Введите значение таймера в секундах",
        validators=[
            DataRequired(message="Обязательное поле"),
        ],
    )
    submit = SubmitField("Установить")


class UserForm(QuartForm):
    telegram_id = IntegerField(
        "Введите Telegram ID пользователя",
        validators=[
            DataRequired(
                message="Обязательное поле",
            )
        ],
    )
    name = StringField(
        "Введите имя пользователя",
        default="Аноним",
        validators=[Optional()],
    )
    role = SelectField(
        choices=[role.value for role in RoleEnum],
        validators=[DataRequired("Обязательное поле")],
    )
    submit = SubmitField("Добавить")
