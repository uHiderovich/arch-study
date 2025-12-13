from fastapi import FastAPI, Query, HTTPException
from typing import List
from app.db import connect_all, disconnect_all, get_db_for_product
from app.models import products
from app.schemas import Product
from contextlib import asynccontextmanager
from app.services.cache import cache_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_all()      # запуск: подключаемся ко всем шардам
    yield                    # приложение работает
    await disconnect_all()   # остановка: корректно закрываем соединения

app = FastAPI(title="Search Service (sharded)", lifespan=lifespan)


# поиск по id (query param product_id)
@app.get("/search", response_model=List[Product])
async def search(
    product_id: int = Query(..., description="Product ID"),
):
    results = []
    cache_response = None

    try:
        cache_response = await cache_service.get(f"product_id:{product_id}")
    except Exception as e:
        print(f"Error getting cache: {e}")

    if cache_response.data:
        results = cache_response.data
    elif product_id is not None:
        # если задана product_id — ищем только в соответствующем шарде
        try:
            db = get_db_for_product(product_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        query = products.select().where(products.c.id == product_id)
        rows = await db.fetch_all(query)
        for r in rows:
            results.append(dict(r))

        try:
            await cache_service.set(f"product_id:{product_id}", results)
        except Exception as e:
            print(f"Error saving cache: {e}")

    return results
