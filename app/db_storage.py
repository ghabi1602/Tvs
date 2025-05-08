from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# initializing sqlalchemy


db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """creates all instances and save to database"""
    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        from .models.student_model import STUDENT
        from .models.prof_model import PROFESSOR
        from .models.course import CLASSES
        from .models.message import MESSAGE

        # Create all tables based on the models
        db.create_all()
