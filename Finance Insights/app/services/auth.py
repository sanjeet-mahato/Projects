from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from argon2 import PasswordHasher
from sqlalchemy import or_, select

from app.models.session import Session
from app.models.user import User
from app.services.database import SessionLocal


password_hasher = PasswordHasher()

SESSION_DURATION = timedelta(days=30)


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
            password_hasher.verify(user.password_hash, password)
        except Exception:
            return None

        user.last_login = datetime.now(UTC)
        db.commit()

        return user


def create_session(username: str) -> str:
    session_id = token_urlsafe(32)
    expires_at = datetime.now(UTC) + SESSION_DURATION

    with SessionLocal() as db:
        session = Session(
            session_id=session_id,
            username=username,
            expires_at=expires_at,
        )

        db.add(session)
        db.commit()

    return session_id


def get_user_from_session(session_id: str) -> User | None:
    with SessionLocal() as db:
        session = db.scalar(
            select(Session).where(
                Session.session_id == session_id,
                Session.expires_at > datetime.now(UTC),
            )
        )

        if not session:
            return None

        user = db.get(User, session.username)

        if not user or not user.is_active:
            return None

        return user


def delete_session(session_id: str) -> None:
    with SessionLocal() as db:
        session = db.get(Session, session_id)

        if session:
            db.delete(session)
            db.commit()