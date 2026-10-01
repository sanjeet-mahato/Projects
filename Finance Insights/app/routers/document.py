from fastapi import APIRouter, Depends

from app.schemas.document import DocumentUpload
from app.services.validator import ValidatedPayload


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    payload: DocumentUpload = Depends(
        ValidatedPayload(
            DocumentUpload,
            content_type="multipart/form-data",
        )
    ),
):
    file = payload.file

    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }