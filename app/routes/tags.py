from flask import Blueprint, render_template
from app.models import Tag

tags_bp = Blueprint("tags", __name__)

@tags_bp.route("/<tag_name>")
def tag_page(tag_name):
    tag = Tag.query.filter_by(name=tag_name.lower()).first_or_404()
    projects = tag.projects  # many-to-many

    return render_template(
        "tags-page.html",
        tag=tag,
        projects=projects
    )