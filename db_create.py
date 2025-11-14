from app import create_app, db
from app.models import User, Project, VolunteerApplication

def init_db():
    app = create_app()

    with app.app_context():
        print(">>> Creating database tables...")
        db.drop_all()    # obriši ako ne želiš reset pri svakom pokretanju
        db.create_all()
        print(">>> Tables created successfully!")

        # OPTIONAL: dodavanje demo projekata
        demo_project = Project(
            title="Park Cleanup",
            short_description="Cleaning up our local community park.",
            description="Volunteers gather to clean trash and improve the environment.",
            location="Community Park"
        )

        db.session.add(demo_project)
        db.session.commit()
        print(">>> Demo project added.")

if __name__ == "__main__":
    init_db()
