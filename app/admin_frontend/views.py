from sqlalchemy.ext.asyncio import AsyncSession
from quart import render_template

from . import app
from crud import products_crud, category_product_crud, portfolio_crud
from .utils import get_file_url, db_session


@app.route("/", methods=["GET"])
async def index():
    return await render_template("base.html")


@app.route("/products")
@db_session
async def get_products(session: AsyncSession):
    """Вывести список всех продуктов."""
    products = await products_crud.get_multi(session)
    return await render_template("products.html", products=products)


@app.route("/products/<int:id>", methods=["GET"])
@db_session
async def get_product_details(session: AsyncSession, id: int):
    """Вывести всю информацию о продукте."""
    product_data = await category_product_crud.get_category_by_product_id(
        id, session
    )
    product = await products_crud.get(id, session)
    for data in product_data:
        if data.media:
            data.media = get_file_url(data.media)
    return await render_template(
        "prdouct_detail.html", product=product, product_data=product_data
    )


@app.route("/projects")
@db_session
async def get_projects(session: AsyncSession):
    projects = await portfolio_crud.get_multi(session)
    return await render_template("projects.html", projects=projects)


@app.route("/projects/<int:id>")
@db_session
async def get_project_details(session: AsyncSession, id: int):
    project = await portfolio_crud.get(id, session)
    return await render_template("project_detail.html", project=project)
