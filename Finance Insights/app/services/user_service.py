from app.models.user import User
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from utils.email_utils import generate_and_send_otp, is_otp_valid, pending_otp

# --------------------------
# Signup
# --------------------------
def prepare_user_signup(username, email, password, profile_name):
    """Check uniqueness, hash password, send OTP, store pending data."""
    if User.query.filter_by(username=username).first():
        return None, "Username already taken"
    if User.query.filter_by(email=email).first():
        return None, "Email already registered"

    password_hash = generate_password_hash(password)
    try:
        generate_and_send_otp(email, username, password_hash, profile_name)
    except Exception as e:
        return None, f"Failed to send OTP: {str(e)}"

    return {"username": username, "email": email, "password_hash": password_hash, "profile_name": profile_name}, None


def verify_email_otp(email, entered_otp):
    """Validate OTP and create user if valid."""
    if email not in pending_otp or not is_otp_valid(email, entered_otp):
        return None, "Invalid or expired OTP"

    data = pending_otp.pop(email)
    new_user = User(
        username=data["username"],
        email=email,
        password_hash=data["password_hash"],
        profile_name=data["profile_name"]
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user, None


# --------------------------
# Login
# --------------------------
def login_user(username_or_email, password):
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    if not user or not check_password_hash(user.password_hash, password):
        return None, "Invalid username or password"
    return user, None


# --------------------------
# Password Reset
# --------------------------
def send_reset_otp(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "Email not registered."
    try:
        generate_and_send_otp(email, username=user.username, password_hash=user.password_hash)
        return True, "OTP sent to your email."
    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"


def reset_password(email, new_password, confirm_password=None):
    """Validate passwords, update DB."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "User not found."
    if confirm_password and new_password != confirm_password:
        return False, "Passwords do not match."
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return True, "Password reset successful."
