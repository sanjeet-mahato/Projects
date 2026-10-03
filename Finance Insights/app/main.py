from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.auth import router as auth_router
from app.routers.document import router as document_router
from app.services.apploadconfig import config
from app.services.exceptions import AuthenticationRequired


app = FastAPI(
    title=config["application"]["name"],
    version=config["application"]["version"],
)


@app.exception_handler(AuthenticationRequired)
async def authentication_required_handler(
    request: Request,
    exc: AuthenticationRequired,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Authentication required",
        },
    )


app.include_router(auth_router)
app.include_router(document_router)