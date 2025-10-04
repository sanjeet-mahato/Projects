import os
from flask import Flask
from app.models.db import init_db

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
    STATIC_DIR = os.path.join(BASE_DIR, "static")

    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.secret_key = "supersecretkey"

    # Initialize database
    init_db(app)

    # Register blueprints
    from app.controllers.auth import auth_bp
    from app.controllers.dashboard import dashboard_bp
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(dashboard_bp, url_prefix="/")

    return app
