from flask import Blueprint, jsonify, abort, request
from flask_login import login_required, current_user
from app.models import Project, User
from app import db
from app.utils.role_required import admin_required

admin_bp = Blueprint("admin", __name__)


# ============================
# PROJECT ACTIONS
# ============================

@admin_bp.route("/project/approve/<int:project_id>", methods=["POST"])
@login_required
@admin_required
def approve_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.approved = True
    project.suspended = False
    db.session.commit()
    return jsonify({"message": "Project approved"}), 200


@admin_bp.route("/project/suspend/<int:project_id>", methods=["POST"])
@login_required
@admin_required
def suspend_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.suspended = True
    db.session.commit()
    return jsonify({"message": "Project suspended"}), 200


@admin_bp.route("/project/delete/<int:project_id>", methods=["POST"])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"}), 200



# ============================
# USER ACTIONS
# ============================

@admin_bp.route("/user/suspend/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def suspend_user(user_id):
    user = User.query.get_or_404(user_id)

    # ne dozvoliti super_admin-u da suspenduje sebe
    if user.id == current_user.id:
        return jsonify({"message": "You cannot suspend yourself"}), 400

    user.role = "suspended"
    db.session.commit()

    return jsonify({"message": "User suspended"}), 200


@admin_bp.route("/user/unsuspend/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def unsuspend_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = "user"
    db.session.commit()
    return jsonify({"message": "User unsuspended"}), 200


@admin_bp.route("/user/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # sprečiti brisanje super_admin naloga
    if user.role == "super_admin":
        return jsonify({"message": "Cannot delete super_admin"}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
