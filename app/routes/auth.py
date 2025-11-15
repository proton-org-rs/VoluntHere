from idlelib.query import Query

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint("auth", __name__)

# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Successfully logged in!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username, name=name, email=email, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/register.html")


# LOGOUT
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("main.index"))

@auth_bp.route("/profile/<string:username>", methods=["GET", "POST"])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    applications = user.applications

    current_projects = []
    finished_projects = []

    for app in applications:
        if app.project.finished:
            finished_projects.append(app)
        else:
            current_projects.append(app)

    return render_template(
        "user/user-profile.html",
        user=user,
        current_projects=current_projects,
        finished_projects=finished_projects
    )

