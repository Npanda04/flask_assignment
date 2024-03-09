from flask import Flask
from app.models import db, ma
from app.routes.userRoutes import user_routes_bp
from flask_migrate import Migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://learn.deepanshu:nCJW4YR9DUPV@ep-orange-pine-a5e2k0bs.us-east-2.aws.neon.tech/flask?sslmode=require"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)

    # Flask-Migrate Initialization
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_routes_bp)

    return app
