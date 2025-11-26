from backend_app.extensions import db, cache
from werkzeug.security import generate_password_hash
from flask import Flask
from flask_cors import CORS    # ✅ CORS import added


def create_app():
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)

    # ✅ Enable CORS for all routes
    CORS(app)   # <-- IMPORTANT LINE

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
                is_admin=True
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
    
    from backend_app.celery import make_celery
    app.celery = make_celery(app)
    
    try:
        import backend_app.tasks
    except:
        pass
    
    return app
