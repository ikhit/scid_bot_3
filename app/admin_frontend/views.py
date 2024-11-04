
from . import app
from crud import products_crud
from core.db import AsyncSessionLocal


@app.route("/", methods = ["GET"])
async def index():
    async with AsyncSessionLocal() as session:
        data = await products_crud.get(1, session)
    return data.name
