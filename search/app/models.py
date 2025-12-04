from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Float
)

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("category_id", Integer, nullable=False),
    Column("price", Float, nullable=False),
    Column("description", String, nullable=True),
)
