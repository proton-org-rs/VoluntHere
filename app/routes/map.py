from flask import Blueprint, jsonify

map_bp = Blueprint("map_bp", __name__)

@map_bp.route("/api/projects")
def get_project_locations():
    from app.models.project import Project

    approved_projects = Project.query.filter_by(approved=True).all()

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "location": p.location
        }
        for p in approved_projects
    ])
