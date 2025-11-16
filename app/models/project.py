from app import db
from datetime import datetime

# ==========================
# MANY-TO-MANY LINK TABLE
# ==========================

project_tags = db.Table(
    'project_tags',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


# ==========================
# TAG MODEL
# ==========================

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # backref prema Project
    projects = db.relationship(
        "Project",
        secondary=project_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


# ==========================
# PROJECT MODEL
# ==========================

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(300))
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.today, nullable=False)
    finished = db.Column(db.Boolean, default=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship("User", back_populates="projects_owned")

    approved = db.Column(db.Boolean, default=False)
    suspended = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("VolunteerApplication", back_populates="project")

    tags = db.relationship(
        "Tag",
        secondary=project_tags,
        back_populates="projects"
    )

    def __repr__(self):
        return f"<Project {self.title}>"
