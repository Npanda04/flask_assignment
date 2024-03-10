import os

from flask import Flask
from app.models import db, ma
from app.routes.userRoutes import user_routes_bp
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv




def create_app():
    app = Flask(__name__)
    load_dotenv()
    CORS(app)

    backend_url = os.getenv("BACKEND_URL")

    app.config["SQLALCHEMY_DATABASE_URI"] = backend_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)

    # Flask-Migrate Initialization
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_routes_bp)

    return app
