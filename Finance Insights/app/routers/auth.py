from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas.auth import LoginRequest, UserResponse
from app.services.auth import (
    authenticate_user,
    create_session,
    delete_session,
    get_user_from_session,
)
from app.services.validator import ValidatedPayload


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=UserResponse)
async def login(
    response: Response,
    payload: LoginRequest = Depends(
        ValidatedPayload(LoginRequest)
    ),
):
    user = authenticate_user(
        payload.username_or_email,
        payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    session_id = create_session(user.username)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
    )

    return user


@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    user = get_user_from_session(session_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return user


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
):
    session_id = request.cookies.get("session_id")

    if session_id:
        delete_session(session_id)

    response.delete_cookie(
        key="session_id",
    )

    return {
        "message": "Logout successful",
    }