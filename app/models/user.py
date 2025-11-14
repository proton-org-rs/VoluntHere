from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    linkedin = db.Column(db.String(120), nullable=True)
    instagram = db.Column(db.String(120), nullable=True)
    github = db.Column(db.String(120), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("VolunteerApplication", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
