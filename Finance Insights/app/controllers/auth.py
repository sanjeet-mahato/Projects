from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, get_flashed_messages
from app.models.user import User
from app.models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from utils.email_utils import generate_and_send_otp, is_otp_valid, pending_otp

auth_bp = Blueprint("auth", __name__)


# --------------------------
# Signup
# --------------------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if username/email already exists
        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="Username already taken")
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already registered")

        # Hash password and generate/send OTP
        password_hash = generate_password_hash(password)
        try:
            generate_and_send_otp(email, username, password_hash)
        except Exception as e:
            return render_template("signup.html", error=f"Failed to send OTP: {str(e)}")

        session["pending_email"] = email
        return redirect(url_for("auth.verify_email"))

    return render_template("signup.html")


# --------------------------
# Verify Email OTP
# --------------------------
@auth_bp.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    email = session.get("pending_email")
    if not email or email not in pending_otp:
        return redirect(url_for("auth.signup"))

    if request.method == "POST":
        entered_otp = request.form.get("otp")
        if is_otp_valid(email, entered_otp):
            data = pending_otp.pop(email)

            # Create new user
            new_user = User(
                username=data["username"],
                email=email,
                password_hash=data["password_hash"]
            )
            db.session.add(new_user)
            db.session.commit()
            session.pop("pending_email")
            flash("Email verified successfully. Please login.", "success")
            return redirect(url_for("auth.login"))
        else:
            return render_template("verify_email.html", error="Invalid or expired OTP")

    return render_template("verify_email.html")


# --------------------------
# Resend OTP
# --------------------------
@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    email = session.get("pending_email")
    if not email or email not in pending_otp:
        return jsonify({"success": False, "message": "No pending verification"}), 400

    try:
        generate_and_send_otp(email)  # Reuse centralized function
        return jsonify({"success": True, "message": "OTP resent successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to resend OTP: {str(e)}"}), 500


# --------------------------
# Login
# --------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username_or_email")
        password = request.form.get("password")

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("dashboard.dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    messages = get_flashed_messages(with_categories=True)
    return render_template("login.html", messages=messages)


# --------------------------
# Logout
# --------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# --------------------------
# Password Reset - Email Entry
# --------------------------
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password_email():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("reset_password_email.html", error="Email not registered.")
        try:
            generate_and_send_otp(email)
            session["reset_email"] = email
            session["reset_verified"] = False
            return redirect(url_for("auth.reset_password_otp"))
        except Exception as e:
            return render_template("reset_password_email.html", error=f"Failed to send OTP: {str(e)}")
    return render_template("reset_password_email.html")


# --------------------------
# Password Reset - OTP Verification
# --------------------------
@auth_bp.route("/reset-password/otp", methods=["GET", "POST"])
def reset_password_otp():
    email = session.get("reset_email")
    if not email:
        return redirect(url_for("auth.reset_password_email"))
    if request.method == "POST":
        otp = request.form.get("otp")
        if not is_otp_valid(email, otp):
            return render_template("reset_password_otp.html", error="Invalid or expired OTP.")
        session["reset_verified"] = True
        return redirect(url_for("auth.reset_password_new"))
    return render_template("reset_password_otp.html")


# --------------------------
# Password Reset - New Password Entry
# --------------------------
@auth_bp.route("/reset-password/new", methods=["GET", "POST"])
def reset_password_new():
    email = session.get("reset_email")
    verified = session.get("reset_verified")
    if not email or not verified:
        return redirect(url_for("auth.reset_password_email"))
    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for("auth.reset_password_email"))
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if not new_password or not confirm_password:
            return render_template("reset_password_new.html", error="Please enter and confirm your new password.")
        if new_password != confirm_password:
            return render_template("reset_password_new.html", error="Passwords do not match.")
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        session.pop("reset_email", None)
        session.pop("reset_verified", None)
        flash("Password successfully reset. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password_new.html")


# --------------------------
# Password Reset - Send OTP (API)
# --------------------------
@auth_bp.route("/send-reset-otp", methods=["POST"])
def send_reset_otp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        email = session.get("reset_email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "Email not registered."}), 400
    try:
        generate_and_send_otp(email)
        return jsonify({"success": True, "message": "OTP sent to your email."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to send OTP: {str(e)}"}), 500
