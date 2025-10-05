from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, get_flashed_messages
from app.services.user_service import (
    prepare_user_signup,
    verify_email_otp,
    login_user,
    send_reset_otp,
    reset_password
)
from utils.email_utils import is_otp_valid, pending_otp

auth_bp = Blueprint("auth", __name__)


# --------------------------
# Signup
# --------------------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")

        profile_name = f"{first_name} {last_name}".strip()
        data, error = prepare_user_signup(username, email, password, profile_name)
        if error:
            return render_template("signup.html", error=error)

        session["pending_email"] = email
        return redirect(url_for("auth.otp"))

    return render_template("signup.html")


# --------------------------
# Login
# --------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username_or_email")
        password = request.form.get("password")

        user, error = login_user(username_or_email, password)
        if error:
            return render_template("login.html", error=error)

        session["user_id"] = user.id
        session["profile_name"] = user.profile_name
        return redirect(url_for("index_bp.index_page"))

    messages = get_flashed_messages(with_categories=True)
    return render_template("login.html", messages=messages)


# --------------------------
# OTP verification/resend
# --------------------------
@auth_bp.route("/otp", methods=["GET", "POST"])
def otp():
    email = session.get("pending_email") or session.get("reset_email")
    if not email:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        entered_otp = request.form.get("otp")
        # Signup OTP verification
        if session.get("pending_email"):
            user, error = verify_email_otp(email, entered_otp)
            if error:
                return render_template("otp.html", error=error)
            session.pop("pending_email", None)
            flash("Email verified successfully. Please login.", "success")
            return redirect(url_for("auth.login"))
        # Password reset OTP verification
        if not is_otp_valid(email, entered_otp):
            return render_template("otp.html", error="Invalid or expired OTP")
        session["reset_verified"] = True
        return redirect(url_for("auth.change_password"))

    return render_template("otp.html")


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    email = session.get("pending_email") or session.get("reset_email")
    if not email:
        return jsonify({"success": False, "message": "No pending OTP"}), 400

    from utils.email_utils import generate_and_send_otp, pending_otp
    from app.models.user import User

    if session.get("pending_email"):
        # Signup OTP resend
        if email not in pending_otp:
            return jsonify({"success": False, "message": "Cannot resend OTP. No pending signup request."}), 400
        # resend OTP using stored username/password_hash/profile_name
        data = pending_otp[email]
        generate_and_send_otp(email, data.get("username"), data.get("password_hash"), data.get("profile_name"))
        return jsonify({"success": True, "message": "OTP resent successfully."}), 200

    if session.get("reset_email"):
        # Reset password OTP resend
        if not User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email not registered."}), 400
        generate_and_send_otp(email)
        return jsonify({"success": True, "message": "OTP resent successfully."}), 200


# --------------------------
# Reset password (email entry)
# --------------------------
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password_route():
    if request.method == "POST":
        email = request.form.get("email")
        success, message = send_reset_otp(email)
        if success:
            session["reset_email"] = email
            session["reset_verified"] = False
            return redirect(url_for("auth.otp"))
        return render_template("reset_password.html", error=message)
    return render_template("reset_password.html")


# --------------------------
# Change password
# --------------------------
@auth_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    email = session.get("reset_email")
    verified = session.get("reset_verified")
    if not email or not verified:
        return redirect(url_for("auth.reset_password_route"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        success, message = reset_password(email, new_password, confirm_password)
        if success:
            session.pop("reset_email", None)
            session.pop("reset_verified", None)
            flash("Password successfully reset. Please login.", "success")
            return redirect(url_for("auth.login"))
        return render_template("change_password.html", error=message)

    return render_template("change_password.html")


# --------------------------
# Logout
# --------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
