from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile("config.py", silent=True)

    db.init_app(app)

    # 🔹 modeli se uvoze kako bi SQLAlchemy registrovao tabele
    from app.models import User, Project, VolunteerApplication

    # 🔹 registracija blueprintova
    from app.routes.main import main_bp
    from app.routes.projects import projects_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
