from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)

from app.models.user import User
from app.schemas.auth import (
    AvailabilityResponse,
    EmailRequest,
    LoginRequest,
    OtpVerificationRequest,
    OtpVerificationResponse,
    SignupRequest,
    UserResponse,
)
from app.services.auth import (
    authenticate_user,
    create_session,
    delete_session,
    get_authenticated_user,
    is_email_available,
    is_username_available,
    send_email_verification_otp,
    send_password_reset_otp,
    signup_user,
    verify_email_verification_otp,
    verify_password_reset_otp,
)
from app.services.exceptions import (
    EmailAlreadyExists,
    InvalidVerificationToken,
    UsernameAlreadyExists,
)
from app.services.validator import validate_content_type


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================================
# EMAIL VERIFICATION
# ============================================================================


@router.post("/send-email-verification-otp")
async def send_email_verification(
    payload: EmailRequest,
    request: Request,
):
    validate_content_type(request)

    try:
        send_email_verification_otp(
            payload.email
        )

    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return {
        "message": "Verification OTP sent successfully"
    }


@router.post(
    "/verify-email-verification-otp",
    response_model=OtpVerificationResponse,
)
async def verify_email_verification(
    payload: OtpVerificationRequest,
    request: Request,
):
    validate_content_type(request)

    return verify_email_verification_otp(
        email=payload.email,
        otp=payload.otp,
    )


# ============================================================================
# SIGNUP
# ============================================================================


@router.post(
    "/signup",
    response_model=UserResponse,
)
async def signup(
    payload: SignupRequest,
    request: Request,
):
    validate_content_type(request)

    try:
        signup_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            profile_name=payload.profile_name,
            verification_token=payload.verification_token,
        )

    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    except InvalidVerificationToken as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "username": payload.username,
        "email": payload.email,
        "profile_name": payload.profile_name,
    }


# ============================================================================
# AVAILABILITY
# ============================================================================


@router.get(
    "/check-username",
    response_model=AvailabilityResponse,
)
def check_username_availability(
    username: str,
):
    available = is_username_available(username)

    return {
        "available": available,
        "message": (
            "Username is available"
            if available
            else "Username already registered"
        ),
    }


@router.get(
    "/check-email",
    response_model=AvailabilityResponse,
)
def check_email_availability(
    email: str,
):
    available = is_email_available(email)

    return {
        "available": available,
        "message": (
            "Email is available"
            if available
            else "Email already registered"
        ),
    }


# ============================================================================
# PASSWORD RESET
# ============================================================================


@router.post("/send-password-reset-otp")
async def send_password_reset(
    payload: EmailRequest,
    request: Request,
):
    validate_content_type(request)

    send_password_reset_otp(
        payload.email
    )

    return {
        "message": (
            "If the email is registered, "
            "a password reset OTP has been sent"
        )
    }


@router.post(
    "/verify-password-reset-otp",
    response_model=OtpVerificationResponse,
)
async def verify_password_reset(
    payload: OtpVerificationRequest,
    request: Request,
):
    validate_content_type(request)

    return verify_password_reset_otp(
        email=payload.email,
        otp=payload.otp,
    )


# ============================================================================
# LOGIN
# ============================================================================


@router.post(
    "/login",
    response_model=UserResponse,
)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
):
    validate_content_type(request)

    user = authenticate_user(
        payload.username_or_email,
        payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    session_id = create_session(
        user.username
    )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
    )

    return user


# ============================================================================
# CURRENT USER
# ============================================================================


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user(
    user: User = Depends(get_authenticated_user),
):
    return user


# ============================================================================
# LOGOUT
# ============================================================================


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    user: User = Depends(get_authenticated_user),
):
    session_id = request.cookies.get("session_id")

    delete_session(session_id)

    response.delete_cookie(
        key="session_id"
    )

    return {
        "message": "Logout successful"
    }