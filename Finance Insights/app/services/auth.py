from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from argon2 import PasswordHasher
from fastapi import Request
from sqlalchemy import or_, select

from app.models.user import User
from app.services.database import SessionLocal
from app.services.email_service import EmailService
from app.services.exceptions import (
    AuthenticationRequired,
    EmailAlreadyExists,
    InvalidVerificationToken,
    UsernameAlreadyExists,
)
from app.services.otp_service import OtpService
from app.services.redis_service import RedisService


password_hasher = PasswordHasher()
redis = RedisService()
email_service = EmailService()
otp_service = OtpService()

SESSION_DURATION = timedelta(days=1)
OTP_TOKEN_DURATION = timedelta(minutes=10)


def get_user_by_username(username: str) -> User | None:
    with SessionLocal() as db:
        return db.scalar(
            select(User).where(User.username == username)
        )


def get_user_by_email(email: str) -> User | None:
    with SessionLocal() as db:
        return db.scalar(
            select(User).where(User.email == email)
        )


def is_username_available(username: str) -> bool:
    return get_user_by_username(username) is None


def is_email_available(email: str) -> bool:
    return get_user_by_email(email) is None


def send_email_verification_otp(email: str) -> None:
    if not is_email_available(email):
        raise EmailAlreadyExists()

    otp = otp_service.generate_otp()

    otp_service.store_otp(
        email=email,
        purpose="email_verification",
        otp=otp,
    )

    email_service.send_email(
        subject="Your OTP for FinanceInsights Signup",
        recipients=[email],
        body=(
            "Dear User,\n\n"
            f"Your OTP is:\n\n{otp}\n\n"
            "This OTP is valid for 5 minutes.\n\n"
            "If you did not request this, please ignore this email.\n\n"
            "FinanceInsights Team"
        ),
    )


def create_otp_token(
    email: str,
    purpose: str,
) -> str:
    token = token_urlsafe(32)

    redis.set(
        f"otp_token:{purpose}:{token}",
        email,
        ttl=int(OTP_TOKEN_DURATION.total_seconds()),
    )

    return token


def get_otp_token_email(
    token: str,
    purpose: str,
) -> str | None:
    return redis.get(
        f"otp_token:{purpose}:{token}"
    )


def delete_otp_token(
    token: str,
    purpose: str,
) -> None:
    redis.delete(
        f"otp_token:{purpose}:{token}"
    )


def verify_email_verification_otp(
    email: str,
    otp: str,
) -> dict:
    result = otp_service.verify_otp(
        email=email,
        purpose="email_verification",
        otp=otp,
    )

    if not result.verified:
        return {
            "verified": False,
            "remaining_attempts": result.remaining_attempts,
            "message": result.message,
        }

    token = create_otp_token(
        email=email,
        purpose="email_verification",
    )

    return {
        "verified": True,
        "remaining_attempts": 0,
        "message": result.message,
        "token": token,
    }


def send_password_reset_otp(email: str) -> None:
    user = get_user_by_email(email)

    if not user:
        return

    otp = otp_service.generate_otp()

    otp_service.store_otp(
        email=email,
        purpose="password_reset",
        otp=otp,
    )

    email_service.send_email(
        subject="Your OTP for FinanceInsights Password Reset",
        recipients=[email],
        body=(
            "Dear User,\n\n"
            f"Your OTP is:\n\n{otp}\n\n"
            "This OTP is valid for 5 minutes.\n\n"
            "If you did not request a password reset, please ignore this email.\n\n"
            "FinanceInsights Team"
        ),
    )


def verify_password_reset_otp(
    email: str,
    otp: str,
) -> dict:
    result = otp_service.verify_otp(
        email=email,
        purpose="password_reset",
        otp=otp,
    )

    if not result.verified:
        return {
            "verified": False,
            "remaining_attempts": result.remaining_attempts,
            "message": result.message,
        }

    token = create_otp_token(
        email=email,
        purpose="password_reset",
    )

    return {
        "verified": True,
        "remaining_attempts": 0,
        "message": result.message,
        "token": token,
    }


def signup_user(
    username: str,
    email: str,
    password: str,
    profile_name: str,
    verification_token: str,
) -> None:
    token_email = get_otp_token_email(
        verification_token,
        "email_verification",
    )

    if not token_email:
        raise InvalidVerificationToken(
            "Invalid or expired email verification token."
        )

    if token_email != email:
        raise InvalidVerificationToken(
            "Email does not match the verified email."
        )

    if not is_username_available(username):
        raise UsernameAlreadyExists()

    if not is_email_available(email):
        raise EmailAlreadyExists()

    password_hash = password_hasher.hash(password)

    with SessionLocal() as db:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            profile_name=profile_name,
        )

        db.add(user)
        db.commit()

    delete_otp_token(
        verification_token,
        "email_verification",
    )


def authenticate_user(
    username_or_email: str,
    password: str,
) -> User | None:
    with SessionLocal() as db:
        user = db.scalar(
            select(User).where(
                or_(
                    User.username == username_or_email,
                    User.email == username_or_email,
                )
            )
        )

        if not user or not user.is_active:
            return None

        try:
            password_hasher.verify(
                user.password_hash,
                password,
            )
        except Exception:
            return None

        user.last_login = datetime.now(UTC)
        db.commit()

        return user


def create_session(username: str) -> str:
    session_id = token_urlsafe(32)

    redis.set(
        f"session:{session_id}",
        username,
        ttl=int(SESSION_DURATION.total_seconds()),
    )

    return session_id


def get_user_from_session(
    session_id: str,
) -> User | None:
    username = redis.get(
        f"session:{session_id}"
    )

    if not username:
        return None

    with SessionLocal() as db:
        user = db.get(User, username)

        if not user or not user.is_active:
            return None

        return user


def get_authenticated_user(request: Request) -> User:
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise AuthenticationRequired()

    user = get_user_from_session(session_id)

    if not user:
        raise AuthenticationRequired()

    return user


def delete_session(session_id: str) -> None:
    redis.delete(
        f"session:{session_id}"
    )


def delete_user_sessions(username: str) -> None:
    for session_key in redis.scan("session:*"):
        session_username = redis.get(session_key)

        if session_username == username:
            redis.delete(session_key)


def reset_password(
    email: str,
    new_password: str,
    reset_token: str,
) -> None:
    token_email = get_otp_token_email(
        reset_token,
        "password_reset",
    )

    if not token_email:
        raise InvalidVerificationToken(
            "Invalid or expired password reset token."
        )

    if token_email != email:
        raise InvalidVerificationToken(
            "Email does not match the verified email."
        )

    with SessionLocal() as db:
        user = db.scalar(
            select(User).where(User.email == email)
        )

        if not user:
            raise InvalidVerificationToken(
                "Invalid password reset request."
            )

        user.password_hash = password_hasher.hash(
            new_password
        )

        db.commit()

        username = user.username

    delete_otp_token(
        reset_token,
        "password_reset",
    )

    delete_user_sessions(username)