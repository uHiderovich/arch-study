from typing import Dict
from databases import Database
from environs import Env

env = Env()
env.read_env()


# Маппинг категорий -> шард
# В примере 5 категорий (1..5) и 3 шарда: распределим категории как [1,2] -> shard1, [3,4] -> shard2, [5] -> shard3
CATEGORY_TO_SHARD = {
    1: "shard1",
    2: "shard1",
    3: "shard2",
    4: "shard2",
    5: "shard3",
}

# Получаем DATABASE_URLs из env (docker-compose задаёт)
SHARD_URLS: Dict[str, str] = {
    "shard1": env("SHARD1_DATABASE_URL"),
    "shard2": env("SHARD2_DATABASE_URL"),
    "shard3": env("SHARD3_DATABASE_URL"),
}

# Создаём Database-инстансы (databases lib)
databases: Dict[str, Database] = {
    name: Database(url) for name, url in SHARD_URLS.items()
}


async def connect_all():
    for db in databases.values():
        await db.connect()


async def disconnect_all():
    for db in databases.values():
        await db.disconnect()


def get_db_for_category(category_id: int) -> Database:
    shard_name = CATEGORY_TO_SHARD.get(category_id)
    if not shard_name:
        # если категория неизвестна — можно назначить fallback
        raise ValueError(f"No shard for category {category_id}")
    return databases[shard_name]
