# filepath: backend_app/controllers/basic_routes.py
from flask import Blueprint, jsonify

# Create blueprint with proper URL prefix
basic_bp = Blueprint("basic_bp", __name__, url_prefix="/")

@basic_bp.route("/")
def home():
    """Home route - returns welcome message"""
    return jsonify({
        "message": "Welcome to the Parking API!",
        "version": "1.0.0",
        "status": "active"
    })

@basic_bp.route("/ping")
def ping():
    """Health check route - returns pong"""
    return jsonify({
        "status": "success",
        "message": "pong"
    })

@basic_bp.route("/health")
def health_check():
    """Detailed health check route"""
    return jsonify({
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "cache": "active"
        }
    })