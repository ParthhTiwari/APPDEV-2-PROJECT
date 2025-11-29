from flask import Flask
from backend_app.extensions import db, cache
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from config import Config
from backend_app.celery import celery_app   # global celery import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    cache.init_app(app)

    with app.app_context():
        from backend_app.models import User, ParkingLot, Spot, Vehicle
        db.create_all()

        if not User.query.filter_by(email="admin@gmail.com").first():
            admin = User(
                name="admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin123"),
                is_admin=True,
            )
            db.session.add(admin)
            db.session.commit()

    from backend_app.controllers.basic_routes import basic_bp
    from backend_app.controllers.user import user_bp
    from backend_app.controllers.admin import admin_bp
    from backend_app.auth import auth_bp

    app.register_blueprint(basic_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

   

    # Beat schedule: daily reminder & monthly report
    celery_app.conf.beat_schedule = {
        "daily-reminders": {
            "task": "send_daily_reminders",
            "schedule": 60 * 60 * 24,  # every 24 hours
        },
        "monthly-reports": {
            "task": "send_monthly_reports",
            "schedule": 60 * 60 * 24 * 30,  # approx 30 days
        },
    }

    # Include flask context in tasks
    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask

    # Flask app can access celery
    app.celery = celery_app

    # Import tasks to register them with celery
    import backend_app.tasks  

    return app


# Convenience import
celery = celery_app
