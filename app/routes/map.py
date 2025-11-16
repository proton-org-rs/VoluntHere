from flask import Blueprint, jsonify

map_bp = Blueprint("map_bp", __name__)

@map_bp.route("/api/projects")
def get_project_locations():
    # ❗❗ Importujemo modele OVDE — izbegava circular import ❗❗
    from app.models.project import Project

    projects = Project.query.all()

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "location": p.location
        }
        for p in projects
    ])
