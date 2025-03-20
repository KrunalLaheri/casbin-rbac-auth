from fastapi import FastAPI
from routers.auth import casbin_router

app = FastAPI()

app.include_router(casbin_router)
