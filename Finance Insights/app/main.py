from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.document import router as documents_router
from app.services.apploadconfig import config


app = FastAPI(
    title=config["application"]["name"],
    version=config["application"]["version"],
)


app.include_router(auth_router)
app.include_router(documents_router)