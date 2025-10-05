from flask import Blueprint, render_template, request, jsonify, session
from app.services.transformer_service import transform_excel_to_json
from io import BytesIO

index_bp = Blueprint("index_bp", __name__)

@index_bp.route("/")
@index_bp.route("/index")
def index_page():
    return render_template("index.html")


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
