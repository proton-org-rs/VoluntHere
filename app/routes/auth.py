from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, VolunteerApplication, Project

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    # === STATISTIKA ===

    # 1) Finished projects where user participated
    finished_projects_count = (
        VolunteerApplication.query
        .join(Project)
        .filter(
            VolunteerApplication.user_id == user.id,
            Project.finished.is_(True)
        ).count()
    )

    # 2) Active volunteerings (approved, not suspended, not finished)
    currently_volunteering_count = (
        VolunteerApplication.query
        .join(Project)
        .filter(
            VolunteerApplication.user_id == user.id,
            Project.finished.is_(False),
            Project.suspended.is_(False),
            Project.approved.is_(True)
        ).count()
    )

    # 3) Projects owned by user (organizing)
    organizing_count = (
        Project.query
        .filter(
            Project.owner_id == user.id,
            Project.finished.is_(False),
            Project.suspended.is_(False)
        ).count()
    )

    stats = {
        "finished": finished_projects_count,
        "volunteering": currently_volunteering_count,
        "organizing": organizing_count
    }

    return render_template(
        "user/user-profile.html",
        user=user,
        stats=stats,
        current_projects=user.applications,   # već koristiš ovo
        finished_projects=[
            app for app in user.applications if app.project.finished
        ]
    )




# # LOGIN
# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#
#         user = User.query.filter_by(email=email).first()
#
#         if user and bcrypt.check_password_hash(user.password_hash, password):
#             login_user(user)
#             flash("Successfully logged in!", "success")
#             return redirect(url_for("main.index"))
#         else:
#             flash("Invalid email or password.", "danger")
#
#     return render_template("auth/login.html")
#
#
# # REGISTER
# @auth_bp.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         name = request.form.get("name")
#         email = request.form.get("email")
#         password = request.form.get("password")
#
#         existing_user = User.query.filter_by(email=email).first()
#
#         if existing_user:
#             flash("Email already registered.", "danger")
#             return redirect(url_for("auth.register"))
#
#         hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
#
#         user = User(username=username, name=name, email=email, password_hash=hashed_pw)
#         db.session.add(user)
#         db.session.commit()
#
#         flash("Account created successfully!", "success")
#         return redirect(url_for("auth.profile"))
#
#     return render_template("auth/register.html")
#
#
# # LOGOUT
# @auth_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("Logged out successfully.", "info")
#     return redirect(url_for("main.index"))
