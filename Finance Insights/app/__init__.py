import os
from flask import Flask
from flask_session import Session
from app.db import init_db, db
import redis

def create_app():
    """
    Application factory function to create and configure the Flask app.
    """
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
    STATIC_DIR = os.path.join(BASE_DIR, "static")

    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR
    )

    # Secret key for sessions and flash messages
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

    # Initialize SQLAlchemy
    init_db(app)

    # Configure server-side sessions using Redis
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        db=int(os.environ.get('REDIS_DB', 0)),
        password=os.environ.get('REDIS_PASSWORD', None)
    )
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    Session(app)


    # Register CLI commands
    from app.commands import register_commands
    register_commands(app)

    # Register Blueprints
    from app.routes.auth_route import auth_bp
    from app.routes.dashboard_route import dashboard_bp
    from app.routes.index_routes import index_bp

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # Optional: add a simple health check route
    @app.route("/ping")
    def ping():
        return "ping", 200

    return app
