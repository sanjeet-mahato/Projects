from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.models.user import User
from app.services.auth import get_authenticated_user


PAGES_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "pages"
)


router = APIRouter(
    tags=["Pages"],
)


def get_page(page_name: str) -> FileResponse:

    page_file = PAGES_DIR / f"{page_name}.html"

    if not page_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )

    return FileResponse(page_file)


# ============================================================
# PUBLIC PAGES
# ============================================================

@router.get("/login")
async def login_page():

    return get_page("login")


@router.get("/signup")
async def signup_page():

    return get_page("signup")


@router.get("/forgot-password")
async def forgot_password_page():

    return get_page("forgot-password")


# ============================================================
# PROTECTED PAGES
# ============================================================

@router.get("/")
@router.get("/home")
async def home(
    user: User = Depends(get_authenticated_user),
):

    return get_page("home")
