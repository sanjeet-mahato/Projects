from flask_sqlalchemy import SQLAlchemy
from utils.config_loader import load_json_config

# Global SQLAlchemy object
db = SQLAlchemy()

# Load MySQL configs
mysql_config = load_json_config("mysql_config.json")
DB_URI = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@" \
         f"{mysql_config.get('host', 'localhost')}/{mysql_config['database']}"

def init_db(app):
    """
    Initialize SQLAlchemy with Flask app
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
