from typing import Any

from fastapi import HTTPException, Request, status
from pydantic import BaseModel, ValidationError


def _raise_validation_error(details: dict[str, str]) -> None:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "message": "Request validation failed",
            "details": details,
        },
    )


def _validate_content_type(
    request: Request,
    expected: str,
) -> None:
    actual = request.headers.get("content-type", "")

    if not actual.startswith(expected):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={
                "message": "Unsupported media type",
                "details": {
                    "content_type": f"Expected {expected}",
                },
            },
        )


async def _extract_json(request: Request) -> Any:
    try:
        return await request.json()
    except Exception:
        _raise_validation_error(
            {"body": "Invalid JSON"}
        )


async def _extract_form(request: Request) -> dict[str, Any]:
    try:
        form = await request.form()

        return {
            key: value
            for key, value in form.multi_items()
        }

    except Exception:
        _raise_validation_error(
            {"body": "Invalid request body"}
        )


def _validate_payload(
    schema: type[BaseModel],
    payload: Any,
) -> BaseModel:
    try:
        return schema.model_validate(payload)

    except ValidationError as exc:
        details = {}

        for error in exc.errors():
            location = ".".join(
                str(value)
                for value in error["loc"]
            )

            field = f"body.{location}" if location else "body"
            details[field] = error["msg"]

        _raise_validation_error(details)


class ValidatedPayload:
    def __init__(
        self,
        schema: type[BaseModel],
        content_type: str = "application/json",
    ):
        self.schema = schema
        self.content_type = content_type

    async def __call__(self, request: Request) -> BaseModel:
        _validate_content_type(
            request,
            self.content_type,
        )

        if self.content_type == "application/json":
            payload = await _extract_json(request)

        elif self.content_type == "multipart/form-data":
            payload = await _extract_form(request)

        else:
            payload = await request.body()

        return _validate_payload(
            self.schema,
            payload,
        )