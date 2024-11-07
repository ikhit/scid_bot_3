from quart import render_template

from . import app
from crud import products_crud, category_product_crud
from core.db import AsyncSessionLocal


@app.route("/", methods=["GET"])
async def index():
    return await render_template("base.html")


@app.route("/porducts")
async def products():
    async with AsyncSessionLocal() as session:
        products = await products_crud.get_multi(session)
    return await render_template("products.html", products=products)


@app.route("/products/<int:product_id>")
async def product_details(product_id):
    async with AsyncSessionLocal() as session:
        product_data = await category_product_crud.get_category_by_product_id(
            product_id, session
        )
        product = await products_crud.get(product_id, session)
    return await render_template(
        "detail.html",
        product=product,
        product_data=product_data,
    )
