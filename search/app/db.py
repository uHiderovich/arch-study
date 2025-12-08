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

SHARDS = SHARD_URLS.keys()
TOTAL_SHARDS = len(SHARDS)

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


def shard_function(product_id: int) -> str:
    return (hash(product_id) % TOTAL_SHARDS) or TOTAL_SHARDS


def get_shard_name(product_id: int) -> str:
    return f"shard{shard_function(product_id)}"


def get_shard_url(product_id: int) -> str:
    shard_name = get_shard_name(product_id)
    return SHARD_URLS.get(shard_name)


def get_db_for_product(product_id: int):
    shard_name = get_shard_name(product_id)
    db = databases.get(shard_name)
    if not db:
        raise ValueError(f"No database found for shard {shard_name}")
    return db
