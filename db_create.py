from app import create_app, db, bcrypt
from app.models import User, Project, VolunteerApplication

def init_db():
    app = create_app()

    with app.app_context():
        print(">>> Resetting database...")
        db.drop_all()
        db.create_all()
        print(">>> Tables created successfully!")

        # -------------------------
        # CREATE DEFAULT USERS
        # -------------------------

        # Password for all demo users:
        default_password = bcrypt.generate_password_hash("password123").decode("utf-8")

        super_admin = User(
            username="superadmin",
            name="Super Administrator",
            email="superadmin@example.com",
            password_hash=default_password,
            role="super_admin"
        )

        admin = User(
            username="admin",
            name="Admin User",
            email="admin@example.com",
            password_hash=default_password,
            role="admin"
        )

        user = User(
            username="john_doe",
            name="John Doe",
            email="john@example.com",
            password_hash=default_password,
            role="user"
        )

        db.session.add_all([super_admin, admin, user])
        db.session.commit()
        print(">>> Default users created.")

        # -------------------------
        # CREATE MULTIPLE PROJECTS
        # -------------------------

        projects = [
            Project(
                title="Park Cleanup",
                short_description="Cleaning up our local community park.",
                description="Volunteers gather to clean trash and improve the environment.",
                location="Central Park",
                owner_id = 1
            ),
            Project(
                title="Community Movie Night",
                short_description="Outdoor cinema for the neighborhood.",
                description="Volunteers organize an outdoor movie screening with snacks.",
                location="Town Square",
                owner_id = 1
            ),
            Project(
                title="STEM Kids Workshop",
                short_description="Robotics workshop for young students.",
                description="Interactive robotics & coding workshop for kids aged 10–14.",
                location="Local School Lab",
                owner_id = 1
            ),
            Project(
                title="Food Drive",
                short_description="Collecting food donations for families in need.",
                description="A community-led initiative that gathers food supplies.",
                location="Donation Center",
                owner_id = 1
            ),
            Project(
                title="Plant a Tree Day",
                short_description="Tree-planting event for cleaner air.",
                description="Volunteers plant young trees in the community forest.",
                location="Forest Park",
                owner_id = 1
            )
        ]

        db.session.add_all(projects)
        db.session.commit()
        print(">>> Demo projects created.")

        print(">>> Database initialization complete!")


if __name__ == "__main__":
    init_db()
