from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(300))
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.today(), nullable = False)
    finished = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved = db.Column(db.Boolean, default=False)
    suspended = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("VolunteerApplication", back_populates="project")

    def __repr__(self):
        return f"<Project {self.title}>"
