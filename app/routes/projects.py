from flask import Blueprint, render_template

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def list_projects():
    return render_template("projects/list.html")
