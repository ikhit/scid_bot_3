from enum import Enum

from quart_wtf import QuartForm, FileRequired
from wtforms import (
    StringField,
    SubmitField,
    URLField,
    ValidationError,
    TextAreaField,
    FileField,
)
from wtforms.validators import DataRequired


class ContentEnum(str, Enum):
    TEXT = "Текст"
    URL = "Ссылка"
    MEDIA = "Картинка"


def validate_name_len(form, field):
    """Валидация длины названия для кнопок."""
    if len(field.data.encode("utf-8")) >= 64:
        raise ValidationError(
            "Слишком длинное название (не поместится в кнопку)."
        )


class BaseForm(QuartForm):
    name = StringField(
        "Введите название",
        validators=[
            DataRequired(message="Обязательное поле"),
            validate_name_len,
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


class MediaForm(TextForm):
    media = FileField(
        validators=[
            FileRequired(),
        ]
    )
