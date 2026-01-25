from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.transformer_service import transform_excel_to_json
from utils.auth_decorator import login_required
from io import BytesIO


index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@index_bp.route("/index")
@login_required
def index_page():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    profile_name = session.get("profile_name", "User")
    return render_template("index.html", profile_name=profile_name)

@index_bp.route("/current-user")
def current_user():
    profile_name = session.get("profile_name", "User")
    return jsonify({"status": "success", "profile_name": profile_name})


@index_bp.route("/upload", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith((".xlsx", ".xls")):
        return jsonify({"status": "error", "message": "Invalid file type"}), 400

    # Read file into memory
    file_stream = BytesIO(file.read())

    # Transform Excel in memory
    result = transform_excel_to_json(file_stream)

    # Store JSON in session temporarily
    if result.get("status") == "success":
        session["transformed_json"] = result

    return jsonify(result)
