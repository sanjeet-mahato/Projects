from app import create_app
from app.models.db import db

app = create_app()

with app.app_context():
    db.create_all()  # ensure tables exist

if __name__ == "__main__":
    app.run(debug=True)
