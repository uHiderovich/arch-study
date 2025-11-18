from typing import List
from .models import Product, User


fake_users_db = {
    "artem": {
        "id": 1,
        "username": "test",
        "email": "test@test.com",
        "hashed_password": "$2b$12$FG9AqWROhXgzYU7tgZTv4e0podTGW47KUHurqnOLVscqM5dO00yPO"
    }
}

fake_products: List[Product] = [
    Product(id=1, name="Laptop", price=1200),
    Product(id=2, name="Phone", price=800),
]
