import jsonify
from flask import Blueprint, render_template, request
from flask import jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Project, VolunteerApplication, Tag
from datetime import datetime
import certification.user_blockchain_service
from random import randint
import asyncio

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
async def edit_project(project_id):
    service = certification.user_blockchain_service.UserBlockchainService()

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

        if not project.finished and request.form.get("finished"):
            # korisniku upisati sertifikat za ovaj projekat
            temp = VolunteerApplication.query.filter_by(project_id=project.id).all()

            users_to_certify = []

            for app in temp:
                if not app.user.certificate_issued:
                    users_to_certify.append(app.user.username)
            
            print(f"\n\nUsers to certify: {users_to_certify}\n\n")

            for username in users_to_certify:
                try:
                    await service.issue_certificate_to_user(username, project.title, randint(4, 16))
                    
                    # Mark as issued only if successful
                    app = VolunteerApplication.query.filter_by(user_id=username, project_id=project.id).first()
                    if app:
                        app.user.certificate_issued = True
                        
                except Exception as e:
                    print(f"Failed to issue certificate to {username}: {e}")
                    # Continue to next user instead of failing entirely

        project.finished = bool(request.form.get("finished"))
        db.session.commit()
        return render_template("projects/edit-project.html", project=project)

@projects_bp.route("/filter/tag/<tag_name>")
def filter_by_tag(tag_name):
    tag_name = tag_name.lower()

    tag = Tag.query.filter_by(name=tag_name).first_or_404()

    projects = (
        Project.query
        .join(Project.tags)
        .filter(
            Tag.name == tag_name,
            Project.approved.is_(True),
            Project.suspended.is_(False),
            Project.finished.is_(False)
        )
        .order_by(Project.created_at.desc())
        .limit(3)
        .all()
    )

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "short_description": p.short_description
        }
        for p in projects
    ])


