from sqlalchemy import create_engine

from app.models import metadata, products
from app.db import SHARD_URLS
from app.db import CATEGORY_TO_SHARD

# Простейшее распределение примеров:
# 5 категорий: 1..5
seed_products = [
    {
        "name": f"Product {i + 1}",
        "category_id": (i % 5) + 1,
        "price": round(10 + i * 2.5, 2),
        "description": f"Description {i + 1}"
    }
    for i in range(15)
]


def create_tables_and_seed():
    # Для каждого шарда создаём таблицу и вставляем продукты, отфильтровав по категории
    for shard_name, url in SHARD_URLS.items():
        engine = create_engine(url)
        metadata.create_all(engine)  # создаст таблицу products в этой БД
        # compute which products belong to this shard
        conn = engine.connect()
        for p in seed_products:
            # проверяем маппинг категорий из db.py — повторим логику
            # простой способ: вставляем только те продукты, которые маппятся к данному шарду
            if CATEGORY_TO_SHARD[p["category_id"]] == shard_name:
                conn.execute(
                    products.insert().values(
                        name=p["name"],
                        category_id=p["category_id"],
                        price=p["price"],
                        description=p["description"]
                    )
                )
        conn.close()
    print("Seeding done.")


if __name__ == "__main__":
    create_tables_and_seed()
