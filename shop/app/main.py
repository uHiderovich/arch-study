from fastapi import FastAPI
from .auth import router as auth_router
from .products import router as products_router
from .users import router as users_router
from .orders import router as orders_router
from contextlib import asynccontextmanager
from .services.notifications.RabbitNotifications import connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await connection.close()


app = FastAPI(title="Mini Shop")

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(orders_router)
