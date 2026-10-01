from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class DocumentUpload(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    file: UploadFile