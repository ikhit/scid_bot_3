from wtforms import ValidationError


def validate_button_len(form, field):
    """Валидация длины названия для кнопок."""
    if len(field.data.encode("utf-8")) >= 64:
        raise ValidationError(
            "Слишком длинное название (не поместится в кнопку)."
        )
