from flask import Blueprint, render_template

from app.models import Project

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def list_projects():
    projects = Project.query.all()
    return render_template("projects/list.html", projects=projects)

@projects_bp.route('/<int:project_id>')
def project_details(project_id):
    project = Project.query.get(project_id)
    return render_template("projects/details.html", project=project)
