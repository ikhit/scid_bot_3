from math import ceil

from quart import render_template, request


def paginate_objects(
    objects: list, page: int = 1, per_page: int = 5
) -> tuple[list[object], int, int]:
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
    add_url: str | None = None,
    details_url: str | None = None,
):
    page = request.args.get("page", 1, type=int)
    paginated_data, total_pages = paginate_objects(data, page=page, per_page=5)

    return await render_template(
        template_name,
        data_list=paginated_data,
        title=title,
        current_page=page,
        total_pages=total_pages,
        endpoint=endpoint,
        add_url=add_url,
        details_url=details_url,
    )
