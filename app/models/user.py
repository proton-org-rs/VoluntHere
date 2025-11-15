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
    profile_pic = db.Column(db.String(500), nullable=True)

    # ✔ Dodato: role = user, admin, super_admin
    role = db.Column(db.String(20), default="user")

    suspended = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("VolunteerApplication", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

    # Helper funkcije
    def is_admin(self):
        return self.role in ["admin", "super_admin"]

    def is_super_admin(self):
        return self.role == "super_admin"

