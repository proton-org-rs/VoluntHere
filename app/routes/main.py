from flask import Blueprint, render_template

from app.models import Project, Tag

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    projects = (
        Project.query
        .filter(Project.suspended == False)
        .filter(Project.approved == True)
        .filter(Project.finished == False)
        .order_by(Project.created_at.desc())
        .all()
    )
    tags = Tag.query.all()
    return render_template("index.html", projects=projects, tags=tags)
