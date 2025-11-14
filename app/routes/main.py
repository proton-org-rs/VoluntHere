from flask import Blueprint, render_template

from app.models import Project

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    projects = (
        Project.query
        .filter(Project.suspended == False)
        .filter(Project.approved == True)
        .order_by(Project.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template("index.html", projects=projects)
