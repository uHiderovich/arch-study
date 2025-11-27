from fastapi import FastAPI
from .router import router

app = FastAPI(title="Payment Service")

app.include_router(router)
