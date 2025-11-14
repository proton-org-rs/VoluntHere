from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(300))
    description = db.Column(db.Text)
    location = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("VolunteerApplication", back_populates="project")

    def __repr__(self):
        return f"<Project {self.title}>"
