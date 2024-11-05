from quart import render_template

from . import app
from crud import products_crud
from core.db import AsyncSessionLocal


@app.route("/", methods=["GET"])
async def index():
    return await render_template("base.html")


@app.route("/porducts")
async def products():
    async with AsyncSessionLocal() as session:
        products = await products_crud.get_multi(session)
    return await render_template("products.html", products=products)
