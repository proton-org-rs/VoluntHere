import jsonify
from flask import Blueprint, render_template, request
from flask import jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Project, VolunteerApplication
from datetime import datetime

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def list_projects():
    projects = (
        Project.query
        .filter(Project.suspended == False)
        .filter(Project.approved == True)
        .order_by(Project.created_at.desc())
        .all()
    )

    return render_template("projects/list.html", projects=projects)

@projects_bp.route('/<int:project_id>')
def project_details(project_id):
    project = Project.query.get(project_id)
    return render_template("projects/details.html", project=project)

@projects_bp.route('/join/<int:project_id>', methods=['POST'])
@login_required
def join_project(project_id):

    project = Project.query.get_or_404(project_id)
    user = current_user

    # Check if already joined
    existing = VolunteerApplication.query.filter_by(
        user_id=user.id,
        project_id=project.id
    ).first()

    if existing:
        return jsonify({'message': 'You already joined this project!'}), 200

    # Create new join
    volunteer = VolunteerApplication(user_id=user.id, project_id=project.id)
    db.session.add(volunteer)
    db.session.commit()

    return jsonify({'message': 'You successfully joined the project!'}), 201

@projects_bp.route('/project-dashboard')
@login_required
def project_dashboard():
    projects = Project.query.order_by(Project.created_at.desc()).filter_by(owner_id=current_user.id).all()
    return render_template("user/projects-dashboard.html",projects=projects)

@projects_bp.route('/edit/<int:project_id>', methods=['POST','GET'])
@login_required
def edit_project(project_id):
    if request.method == "GET":
        if Project.query.filter_by(id=project_id).first().owner_id != current_user.id:
            return jsonify({'message': 'You do not have permission to edit this project!'}), 403
        project = Project.query.filter_by(id=project_id).first()
        return render_template("projects/edit-project.html", project=project)
    else:
        project = Project.query.filter_by(id=project_id).first()
        if Project.query.filter_by(id=project_id).first().owner_id != current_user.id:
            return jsonify({'message': 'You do not have permission to edit this project!'}), 403
        project.title = request.form['title']
        project.short_description = request.form['short_description']
        project.description = request.form['description']
        project.location = request.form['location']
        project.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        project.finished = bool(request.form.get("finished"))
        db.session.commit()
        return render_template("projects/edit-project.html", project=project)



