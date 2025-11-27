from fastapi import FastAPI
from .router import router

app = FastAPI(title="Shipping Service")

app.include_router(router)
