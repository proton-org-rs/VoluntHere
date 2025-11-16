import os
from dotenv import load_dotenv
load_dotenv()

from flask_session import Session
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from .config import Config
from app.routes.map import map_bp

# === Flask extensions ===
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
oauth = OAuth()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile("config.py", silent=True)

    # --- 🚀 ENABLE SESSION STORAGE ---
    Session(app)   # ← OVO JE KLJUČNO ZA AUTH0 state check

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    oauth.init_app(app)

    # Import modela zbog LoginManager-a
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('main.index'))

    # AUTH0 CONFIG
    app.auth0 = oauth.register(
        "auth0",
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f"https://auth.volunthere.proton.org.rs/.well-known/openid-configuration",
    )

    # Blueprintovi
    from app.routes.main import main_bp
    from app.routes.projects import projects_bp
    from app.routes.admin import admin_bp
    from app.routes.search import search_bp
    from app.routes.tags import tags_bp
    from app.routes.auth0 import auth0_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(auth0_bp, url_prefix="/auth")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(tags_bp, url_prefix="/tags")
    app.register_blueprint(map_bp)

    return app
