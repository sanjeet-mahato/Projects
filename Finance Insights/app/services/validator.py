from fastapi import HTTPException, Request, status


def validate_content_type(
    request: Request,
    expected: str = "application/json",
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