from math import ceil

from quart import render_template, request


def paginate_objects(
    objects: list, page: int = 1, per_page: int = 5
) -> tuple[list[object], int, int]:
    """
    Разбивает список объектов на страницы для пагинации.

    :param objects: Список объектов, который необходимо разбить на страницы.
    :param page: Номер текущей страницы (по умолчанию 1).
    :param per_page: Количество объектов на странице (по умолчанию 5).
    :return: Кортеж из двух элементов:
             1. Список объектов для текущей страницы.
             2. Общее количество страниц.
    """
    total_count = len(objects)
    total_pages = ceil(total_count / per_page)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * per_page
    paginated_objects = objects[offset : offset + per_page]
    return paginated_objects, total_pages


async def get_paginated_data_and_render(
    data: list,
    template_name: str,
    title: str,
    endpoint: str,
    **kwargs,
):
    """
    Получает данные, выполняет пагинацию и рендерит страницу с использованием шаблона.

    :param data: Список данных, которые необходимо отобразить.
    :param template_name: Имя шаблона для рендеринга.
    :param title: Заголовок страницы.
    :param endpoint: URL-эндпоинт, используемый для построения ссылок на страницы.
    :param kwargs: Дополнительные параметры для передачи в шаблон.
    :return: Отрендеренная страница с данными и пагинацией.
    """
    data = [obj.verbosed_dict() for obj in data]
    page = request.args.get("page", 1, type=int)
    paginated_data, total_pages = paginate_objects(data, page=page, per_page=5)

    return await render_template(
        template_name,
        data_list=paginated_data,
        title=title,
        current_page=page,
        total_pages=total_pages,
        endpoint=endpoint,
        **kwargs,
    )
