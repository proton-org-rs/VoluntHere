from app import db
from datetime import datetime

class VolunteerApplication(db.Model):
    __tablename__ = "volunteer_applications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="applications")
    project = db.relationship("Project", back_populates="applications")

    def __repr__(self):
        return f"<VolunteerApplication u={self.user_id} p={self.project_id}>"
