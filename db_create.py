from app import create_app, db, bcrypt
from app.models import User, Project, Tag

def init_db():
    app = create_app()

    with app.app_context():
        print(">>> Resetting database...")
        db.drop_all()
        db.create_all()
        print(">>> Tables created successfully!")

        # =====================================================
        # DEFAULT USERS
        # =====================================================

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

        # =====================================================
        # TAGS
        # =====================================================

        tag_names = [
            "cleanup", "environment", "education", "kids", "community",
            "charity", "outdoor", "forest", "stem", "tech", "animals"
        ]

        tags = {name: Tag(name=name) for name in tag_names}
        db.session.add_all(tags.values())
        db.session.commit()
        print(">>> Tags created.")

        # helper funkcija za dodelu tagova
        def get_tags(*names):
            return [tags[name] for name in names if name in tags]

        # =====================================================
        # PROJECTS
        # =====================================================

        projects = [
            Project(
                title="Park Cleanup",
                short_description="Cleaning up our local community park.",
                description="Volunteers gather to clean trash and improve the environment.",
                location="Timișoara 300028",
                owner_id=1,
                approved=True,
                tags=get_tags("cleanup", "environment", "community")
            ),
            Project(
                title="Community Movie Night",
                short_description="Outdoor cinema for the neighborhood.",
                description="Volunteers organize an outdoor movie screening with snacks.",
                location="Piața Victoriei, Timișoara",
                owner_id=1,
                approved=True,
                tags=get_tags("community", "outdoor")
            ),
            Project(
                title="STEM Kids Workshop",
                short_description="Robotics workshop for young students.",
                description="Interactive robotics & coding workshop for kids aged 10–14.",
                location="Strada Doctor Iosif Nemoianu 5, Timișoara",
                owner_id=1,
                approved=True,
                tags=get_tags("STEM", "tech", "kids", "education")
            ),
            Project(
                title="Food Drive",
                short_description="Collecting food donations for families in need.",
                description="A community-led initiative to gather food supplies.",
                location="Strada Alexandru Odobescu 3, Timișoara 300425",
                owner_id=1,
                approved=True,
                tags=get_tags("charity", "community")
            ),
            Project(
                title="Plant a Tree Day",
                short_description="Tree-planting event for cleaner air.",
                description="Volunteers plant young trees in the community forest.",
                location="Splaiul Nicolae Titulescu 1, Timișoara",
                owner_id=1,
                approved=True,
                tags=get_tags("environment", "forest", "outdoor")
            ),
            Project(  # jedan PENDING project
                title="Animal Shelter Help",
                short_description="Assist local animal shelter with care tasks.",
                description="Feeding, grooming, and playing with shelter animals.",
                location="Piața Victoriei 4, Timișoara 300006",
                owner_id=1,
                approved=False,
                tags=get_tags("animals", "charity")
            )
        ]

        db.session.add_all(projects)
        db.session.commit()
        print(">>> Projects with tags added successfully.")

        print(">>> Database initialization complete!")


if __name__ == "__main__":
    init_db()
