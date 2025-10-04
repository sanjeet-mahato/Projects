from datetime import datetime, UTC
from app.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    profile_name = db.Column(db.String(100))

    def __repr__(self):
        return f"<User {self.username}>"
