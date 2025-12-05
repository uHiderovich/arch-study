from sqlalchemy import create_engine

from app.models import metadata, products
from app.db import SHARD_URLS
from app.db import get_shard_url

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
    # Создаём таблицы на всех шард-базах
    for shard_name, url in SHARD_URLS.items():
        engine = create_engine(url)
        metadata.create_all(engine)
    # Вставляем продукты, определяя шард через хэш
    for i, product in enumerate(seed_products):
        product_id = i + 1
        shard_url = get_shard_url(product_id)
        engine = create_engine(shard_url)
        with engine.connect() as conn:
            conn.execute(
                products.insert().values(
                    id=product_id,
                    name=product["name"],
                    price=product["price"],
                    category_id=product["category_id"],
                    description=product["description"]
                )
            )
            print(f"Inserted {product['name']} into {shard_url}")
    print("Seeding done.")


if __name__ == "__main__":
    create_tables_and_seed()
