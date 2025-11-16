from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
from app.routes.map import map_bp

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile("config.py", silent=True)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('main.index'))  # login view

    from app.models import User, Project, VolunteerApplication

    from app.routes.main import main_bp
    from app.routes.projects import projects_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.search import search_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(map_bp)

    return app
