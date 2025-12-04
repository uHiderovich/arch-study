from fastapi import FastAPI, Query, HTTPException
from typing import List
from app.db import connect_all, disconnect_all, get_db_for_category
from app.models import products
from app.schemas import Product
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_all()      # запуск: подключаемся ко всем шардам
    yield                    # приложение работает
    await disconnect_all()   # остановка: корректно закрываем соединения

app = FastAPI(title="Search Service (sharded)", lifespan=lifespan)


# поиск по имени (query param q), необязательный category (если указан — идём в соответствующий шард)
@app.get("/search", response_model=List[Product])
async def search(
    q: str = Query("", description="search text"),
    category: int | None = Query(None)
):
    q_str = f"%{q}%"
    results = []

    # если задана категория — ищем только в соответствующем шарде
    if category is not None:
        try:
            db = get_db_for_category(category)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        query = products.select().where(
            products.c.name.ilike(q_str),
            products.c.category_id == category
        )
        rows = await db.fetch_all(query)
        for r in rows:
            results.append(dict(r))
        return results

    # если категория не задана — агрегируем по всем шардам (сканируем шарды)
    from app.db import databases
    for db in databases.values():
        rows = await db.fetch_all(products.select().where(
            products.c.name.ilike(q_str)
        ))
        for r in rows:
            results.append(dict(r))
    return results
