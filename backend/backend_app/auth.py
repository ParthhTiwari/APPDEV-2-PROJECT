# filepath: backend_app/auth.py
from flask import Blueprint, request, jsonify
from backend_app.models import User
from backend_app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

# Hardcoded admin credentials (for initial setup)
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "name, email and password required"}), 400

    if email == ADMIN_EMAIL:
        return jsonify({"error": "cannot register reserved admin email"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "user already exists"}), 400

    hashed = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed, is_admin=False)
    db.session.add(user)
    db.session.commit()
    
    # Generate token for new user
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'])
    
    return jsonify({
        "message": "registered", 
        "user_id": user.id,
        "token": token
    }), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email & password required"}), 400

    # Prefer DB user (supports hashed or legacy plaintext)
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password) or user.password == password:
            # Generate token for user
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.config['SECRET_KEY'])
            
            return jsonify({
                "message": "login_success",
                "user_id": user.id,
                "is_admin": bool(user.is_admin),
                "token": token
            }), 200
        return jsonify({"error": "invalid credentials"}), 401

        # Check for admin login
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        
        admin_user = User.query.filter_by(email=ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                name="admin",
                email=ADMIN_EMAIL,
                password=generate_password_hash(ADMIN_PASSWORD),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
        
        # Generate token for admin
        token = jwt.encode({
            'user_id': admin_user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({
            "message": "admin_login", 
            "email": email, 
            "is_admin": True,
            "user_id": admin_user.id,
            "token": token
        }), 200

    return jsonify({"error": "invalid credentials"}), 401