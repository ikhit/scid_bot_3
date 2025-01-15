from quart import render_template, Blueprint
from sqlalchemy.ext.asyncio import AsyncSession

from admin_frontend.utils import (
    db_session,
    delete_item,
    get_image_url,
)
from admin_frontend.form_handlers import (
    add_product_media_form,
    add_product_text_form,
    add_product_url_form,
    add_text_form,
    update_media_form,
    update_text_form,
    update_url_form,
)
from admin_frontend.pagination import get_paginated_data_and_render
from crud import category_product_crud, products_crud


products = Blueprint("products", __name__)


@products.route("/")
@db_session
async def get_products(session: AsyncSession):
    """
    Обрабатывает запрос на получение списка всех продуктов и услуг.
    Функция извлекает все продукты из базы данных и отображает их на странице
    с пагинацией. Также предоставляет возможность добавления нового продукта.
    """
    products = await products_crud.get_multi(session)
    return await get_paginated_data_and_render(
        data=products,
        template_name="bot_data/list.html",
        title="Список продуктов и услуг",
        endpoint=".get_products",
        add_url=".add_product",
        details_url=".get_product_details",
    )


@products.route("/<int:id>")
@db_session
async def get_product_details(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на отображение подробной информации о продукте.
    Функция извлекает данные о продукте по ID и информацию о его категории. 
    При наличии медиа-данных, они обрабатываются для отображения изображения.
    """
    product_data = await category_product_crud.get_category_by_product_id(
        id, session
    )
    product = await products_crud.get(id, session)
    for data in product_data:
        if data.media:
            data.media = get_image_url(data.media)
    return await render_template(
        "bot_data/card.html",
        item=product,
        item_data=product_data,
        delete_url=".delete_product",
    )


@products.route("/add-product", methods=["GET", "POST"])
@db_session
async def add_product(session: AsyncSession):
    """
    Обрабатывает запрос на добавление нового продукта.
    Если запрос GET, отображается форма для добавления нового продукта.
    Если запрос POST, форма отправляется для обработки.
    """
    return await add_text_form(session, products_crud, ".get_product_details")


@products.route("/<int:id>/delete")
@db_session
async def delete_product(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на удаление продукта.
    Функция удаляет продукт по заданному ID из базы данных и перенаправляет 
    на список продуктов.
    """
    return await delete_item(session, products_crud, id, ".get_products")


@products.route("/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_product(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на обновление информации о продукте.
    Если запрос GET, отображается форма для обновления информации о продукте.
    Если запрос POST, форма отправляется для обработки.
    """
    return await update_text_form(
        session, products_crud, id, ".get_product_details"
    )


@products.route("/<int:id>/category/add-media", methods=["GET", "POST"])
@db_session
async def add_product_media(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на добавление медиа-данных (например, изображений)
    к продукту. Если запрос GET, отображается форма для добавления 
    медиа-данных. Если запрос POST, форма отправляется для обработки.
    """
    return await add_product_media_form(session, ".get_product_details", id)


@products.route("/<int:id>/category/add-url", methods=["GET", "POST"])
@db_session
async def add_product_url(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на добавление URL-адреса к продукту.
    Если запрос GET, отображается форма для добавления URL.
    Если запрос POST, форма отправляется для обработки.
    """
    return await add_product_url_form(session, ".get_product_details", id)


@products.route("/<int:id>/category/add-text", methods=["GET", "POST"])
@db_session
async def add_product_text(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на добавление текстовых данных к продукту.
    Если запрос GET, отображается форма для добавления текста.
    Если запрос POST, форма отправляется для обработки.
    """
    return await add_product_text_form(session, ".get_product_details", id)


@products.route("/category/<int:id>/update", methods=["GET", "POST"])
@db_session
async def update_category(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на обновление информации о категории продукта.
    Функция обновляет данные о категории, включая медиа, URL или текстовые 
    данные, в зависимости от наличия этих данных в категории.
    """
    category = await category_product_crud.get(id, session)
    if category.url:
        return await update_url_form(
            session,
            category_product_crud,
            id,
            ".get_product_details",
            category.product_id,
        )
    if not category.media:
        return await update_text_form(
            session,
            category_product_crud,
            id,
            ".get_product_details",
            category.product_id,
        )
    else:
        return await update_media_form(
            session,
            category_product_crud,
            id,
            ".get_product_details",
            category.product_id,
        )


@products.route("/category/<int:id>/delete", methods=["GET", "POST"])
@db_session
async def delete_category(session: AsyncSession, id: int):
    """
    Обрабатывает запрос на удаление категории продукта.
    Функция удаляет категорию по заданному ID и перенаправляет на страницу
    с продуктами.
    """
    category = await category_product_crud.get(id, session)
    return await delete_item(
        session,
        category_product_crud,
        id,
        ".get_product_details",
        category.product_id,
    )
