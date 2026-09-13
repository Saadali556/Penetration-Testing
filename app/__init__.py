import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    secret_key = os.environ.get("SECRET_KEY")

    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is required")

    app.config["SECRET_KEY"] = secret_key

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secureshop.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False

    db.init_app(app)
    csrf.init_app(app)

    Talisman(
        app,
        force_https=False
    )

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app.models import (
            User,
            Product,
            CartItem,
            Order,
            OrderItem
        )

        db.create_all()

    return app
