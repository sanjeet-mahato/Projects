from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.auth_decorator import login_required
from io import BytesIO
from app.models.statement_parser import BankStatementParser
import pandas as pd
import redis
import json
import os


# Redis client for direct DataFrame storage
def get_redis_client():
    """Get Redis client for DataFrame storage"""
    return redis.Redis(
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        db=int(os.environ.get('REDIS_DB', 0)),
        password=os.environ.get('REDIS_PASSWORD', None),
        decode_responses=True  # For JSON serialization
    )


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

    # Parse Excel using BankStatementParser
    parser = BankStatementParser(file_stream=file_stream)
    df_transactions = parser.get_transaction_table()

    # Get Redis client
    redis_client = get_redis_client()

    # Create unique key for this user's data (using session ID or user ID)
    user_id = session.get("user_id", "anonymous")
    redis_key = f"transaction_data:{user_id}"
    print(f"Redis Key: {redis_key}")

    # Convert DataFrame to JSON-serializable format and store in Redis
    transaction_data = {
        "data": df_transactions.to_dict('records'),  # List of dicts
        "columns": list(df_transactions.columns),
        "dtypes": {col: str(dtype) for col, dtype in df_transactions.dtypes.items()},
        "total_transactions": len(df_transactions),
        "timestamp": pd.Timestamp.now().isoformat()
    }

    # Store in Redis with 24 hour expiration
    redis_client.setex(redis_key, 86400, json.dumps(transaction_data))

    # Store only the Redis key in Flask session (not the data)
    session["transaction_redis_key"] = redis_key

    # Return success with basic info
    return jsonify({
        "status": "success",
        "total_transactions": len(df_transactions),
        "columns": list(df_transactions.columns),
        "redis_key": redis_key
    })

@index_bp.route("/get-dataframe", methods=["GET"])
@login_required
def get_dataframe():
    """Get the stored pandas DataFrame as JSON for testing"""
    # Get Redis key from session
    redis_key = session.get("transaction_redis_key")
    if not redis_key:
        return jsonify({"status": "error", "message": "No data uploaded"}), 404

    # Get data from Redis
    redis_client = get_redis_client()
    data_json = redis_client.get(redis_key)
    if not data_json:
        return jsonify({"status": "error", "message": "Data expired or not found"}), 404

    try:
        transaction_data = json.loads(data_json)
        return jsonify({
            "status": "success",
            "data": transaction_data["data"],
            "total_transactions": transaction_data["total_transactions"],
            "columns": transaction_data["columns"],
            "timestamp": transaction_data.get("timestamp")
        })
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Invalid data format"}), 500


def get_transaction_dataframe():
    """Helper function to reconstruct DataFrame from Redis data"""
    # Get Redis key from session
    redis_key = session.get("transaction_redis_key")
    if not redis_key:
        return None

    # Get data from Redis
    redis_client = get_redis_client()
    data_json = redis_client.get(redis_key)
    if not data_json:
        return None

    try:
        transaction_data = json.loads(data_json)
        # Reconstruct DataFrame from stored data
        df = pd.DataFrame(transaction_data["data"])

        # Restore dtypes if needed (basic restoration)
        for col, dtype_str in transaction_data.get("dtypes", {}).items():
            if col in df.columns:
                if 'float' in dtype_str:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif 'int' in dtype_str:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

        return df
    except (json.JSONDecodeError, KeyError):
        return None
