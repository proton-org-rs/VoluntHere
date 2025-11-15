from flask import Blueprint, request, render_template, jsonify
from app.models import User, Project, Tag
from sqlalchemy import or_

search_bp = Blueprint("search", __name__)

@search_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search/results.html", users=[], projects=[], query="")

    # Pretraga usera
    users = User.query.filter(
        or_(
            User.username.ilike(f"%{query}%"),
            User.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%")
        )
    ).all()

    # Pretraga projekata
    projects = Project.query.filter(
        or_(
            Project.title.ilike(f"%{query}%"),
            Project.short_description.ilike(f"%{query}%"),
            Project.location.ilike(f"%{query}%")
        )
    ).all()

    return render_template(
        "search/results.html",
        users=users,
        projects=projects,
        query=query
    )

@search_bp.route("/search/ajax")
def search_ajax():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"users": [], "projects": [], "tags": []})

    # User search
    users = User.query.filter(
        or_(
            User.username.ilike(f"%{query}%"),
            User.name.ilike(f"%{query}%")
        )
    ).limit(5).all()

    # Project search
    projects = Project.query.filter(
        or_(
            Project.title.ilike(f"%{query}%"),
            Project.short_description.ilike(f"%{query}%"),
            Project.location.ilike(f"%{query}%")
        )
    ).limit(5).all()

    # Tag search
    tags = Tag.query.filter(
        Tag.name.ilike(f"%{query}%")
    ).limit(5).all()

    return jsonify({
        "users": [
            {"id": u.id, "username": u.username, "name": u.name}
            for u in users
        ],
        "projects": [
            {"id": p.id, "title": p.title, "desc": p.short_description}
            for p in projects
        ],
        "tags": [
            {"name": t.name}
            for t in tags
        ]
    })


