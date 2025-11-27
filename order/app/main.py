from fastapi import FastAPI
from .router import router

app = FastAPI(title="Order Service")

app.include_router(router)
