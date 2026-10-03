from fastapi import APIRouter, Depends, File, Request, UploadFile

from app.models.user import User
from app.services.auth import get_authenticated_user
from app.services.validator import validate_content_type


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    user: User = Depends(get_authenticated_user),
):
    validate_content_type(
        request,
        "multipart/form-data",
    )

    return {
        "username": user.username,
        "filename": file.filename,
        "content_type": file.content_type,
    }