from flask import Blueprint, request, jsonify
from backend_app import db
from backend_app.models import ParkingLot, Spot, Vehicle, User
from datetime import datetime
from backend_app.auth import ADMIN_EMAIL, ADMIN_PASSWORD
from werkzeug.security import check_password_hash
import jwt
import datetime
from flask import current_app

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# -------------------------------------------------
# ADMIN AUTH MIDDLEWARE
# -------------------------------------------------
@admin_bp.before_request
def require_admin():
    # --- CORS preflight ---
    if request.method == "OPTIONS":
        return '', 200

    # --- Auth check for other requests ---
    email = request.headers.get("X-Admin-Email")
    pwd = request.headers.get("X-Admin-Password")

    # Hardcoded fallback admin
    if email == ADMIN_EMAIL and pwd == ADMIN_PASSWORD:
        # For admin, we need to find or create the admin user
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
        
        # Add token to request context for use in endpoints
        request.admin_token = token
        return None

    # Database admin support
    if email:
        admin_user = User.query.filter_by(email=email, is_admin=True).first()
        if admin_user:
            # Allow hashed or plain password (for initial testing)
            if check_password_hash(admin_user.password, pwd) or admin_user.password == pwd:
                # Generate token for admin
                token = jwt.encode({
                    'user_id': admin_user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, current_app.config['SECRET_KEY'])
                
                # Add token to request context
                request.admin_token = token
                return None

    return jsonify({"error": "Admin credentials required (X-Admin-Email & X-Admin-Password)"}), 401



# -------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------
@admin_bp.get("/dashboard")
def admin_dashboard():
    total_users = User.query.count()
    total_lots = ParkingLot.query.count()
    total_spots = Spot.query.count()
    available_spots = Spot.query.filter_by(is_available=True).count()
    active_vehicles = Vehicle.query.filter_by(exit_time=None).count()

    # recent activity
    recent = Vehicle.query.order_by(Vehicle.entry_time.desc()).limit(5).all()
    recent_data = []

    for v in recent:
        user = User.query.get(v.user_id)
        spot = Spot.query.get(v.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None

        recent_data.append({
            "vehicle_id": v.id,
            "number_plate": v.number_plate,
            "user": user.name if user else None,
            "lot": lot.name if lot else None,
            "spot": spot.spot_number if spot else None,
            "entry_time": v.entry_time.strftime("%Y-%m-%d %H:%M:%S") if v.entry_time else None,
            "status": "Parked" if v.exit_time is None else "Exited"
        })

    # Get the admin token from request context
    token = getattr(request, 'admin_token', None)

    return jsonify({
        "message": "Admin Dashboard Data",
        "token": token,  # Include token in response
        "stats": {
            "total_users": total_users,
            "total_lots": total_lots,
            "total_spots": total_spots,
            "available_spots": available_spots,
            "currently_parked": active_vehicles
        },
        "recent_activity": recent_data
    }), 200

# -------------------------------------------------
# CREATE LOT + AUTO SPOTS
# -------------------------------------------------
@admin_bp.post("/create_lot")
def create_lot():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    location = data.get("location")
    price = data.get("price")
    max_spots = data.get("max_spots")

    if not all([name, location, price, max_spots]):
        return jsonify({"error": "All fields required"}), 400

    try:
        price = float(price)
        max_spots = int(max_spots)
        if max_spots <= 0:
            raise ValueError
    except Exception:
        return jsonify({"error": "Invalid price or max_spots"}), 400

    # Create lot
    lot = ParkingLot(name=name, location=location, price=price, max_spots=max_spots)
    db.session.add(lot)
    db.session.flush()  # get lot.id before commit

    # Create spots
    spots = [Spot(spot_number=i, lot_id=lot.id, is_available=True)
             for i in range(1, max_spots + 1)]
    db.session.add_all(spots)
    db.session.commit()

    return jsonify({"message": "Parking Lot & Spots Created!", "lot_id": lot.id}), 201


# -------------------------------------------------
# GET ALL LOTS
# -------------------------------------------------
# filepath: backend_app/admin.py

# Modify get_lots endpoint to match frontend expectations
@admin_bp.get("/lots")
def get_lots():
    lots = ParkingLot.query.all()
    out = {
        "lots": []  # Frontend expects a "lots" key
    }

    for lot in lots:
        out["lots"].append({
            "lot_id": lot.id,  # Frontend expects "lot_id" not "id"
            "name": lot.name,
            "location": lot.location,
            "price": lot.price,
            "max_spots": lot.max_spots,
            "total_spots": len(lot.spots),
            "available_spots": sum(1 for s in lot.spots if s.is_available),
        })

    return jsonify(out), 200


# -------------------------------------------------
# GET ONE LOT
# -------------------------------------------------
@admin_bp.get("/lot/<int:lot_id>")
def get_single_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    spots_data = [{
        "id": s.id,
        "spot_number": s.spot_number,
        "is_available": s.is_available
    } for s in lot.spots]

    return jsonify({
        "id": lot.id,
        "name": lot.name,
        "location": lot.location,
        "price": lot.price,
        "max_spots": lot.max_spots,
        "total_spots": len(lot.spots),
        "available_spots": sum(1 for s in lot.spots if s.is_available),
        "spots": spots_data
    }), 200


# -------------------------------------------------
# GET SPOTS OF A LOT
# -------------------------------------------------
@admin_bp.get("/lot/<int:lot_id>/spots")
def get_lot_spots(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    spots_data = [{
        "id": s.id,
        "spot_number": s.spot_number,
        "is_available": s.is_available
    } for s in lot.spots]

    return jsonify({
        "id": lot.id,
        "name": lot.name,
        "location": lot.location,
        "price": lot.price,
        "total_spots": len(lot.spots),
        "available_spots": sum(1 for s in lot.spots if s.is_available),
        "spots": spots_data
    }), 200


# -------------------------------------------------
# UPDATE LOT
# -------------------------------------------------
@admin_bp.put("/lot/<int:lot_id>")
def update_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    data = request.get_json(force=True) or {}

    # 1) Basic fields update
    lot.name = data.get("name", lot.name)
    lot.location = data.get("location", lot.location)

    if "price" in data:
        try:
            lot.price = float(data["price"])
        except:
            return jsonify({"error": "Invalid price"}), 400

    # 2) Max spots update + auto delete logic
    if "max_spots" in data:
        try:
            new_max = int(data["max_spots"])
        except:
            return jsonify({"error": "Invalid max_spots"}), 400

        if new_max < 0:
            return jsonify({"error": "max_spots cannot be negative"}), 400

        current_count = len(lot.spots)

        # -------------------------------
        # CASE 0: new_max == 0 → Auto Delete Logic
        # -------------------------------
        if new_max == 0:
            occupied = Spot.query.filter(
                Spot.lot_id == lot_id,
                Spot.is_available == False
            ).count()

            if occupied > 0:
                return jsonify({
                    "error": "Cannot delete lot: some spots are still occupied"
                }), 400

            # Delete all spots of this lot
            Spot.query.filter_by(lot_id=lot_id).delete()

            # Delete the lot itself
            db.session.delete(lot)
            db.session.commit()

            return jsonify({"message": "Parking Lot deleted successfully"}), 200

        # -------------------------------
        # CASE 1: Increase spots
        # -------------------------------
        if new_max > current_count:
            for i in range(current_count + 1, new_max + 1):
                db.session.add(Spot(spot_number=i, lot_id=lot.id, is_available=True))

        # -------------------------------
        # CASE 2: Decrease spots
        # -------------------------------
        elif new_max < current_count:
            occupied = Spot.query.filter(
                Spot.lot_id == lot_id,
                Spot.spot_number > new_max,
                Spot.is_available == False
            ).count()

            if occupied > 0:
                return jsonify({
                    "error": "Cannot reduce spots: some higher-numbered spots are occupied"
                }), 400

            Spot.query.filter(
                Spot.lot_id == lot_id,
                Spot.spot_number > new_max
            ).delete(synchronize_session=False)

        lot.max_spots = new_max

    db.session.commit()
    return jsonify({"message": "Parking Lot Updated"}), 200


# -------------------------------------------------
# DELETE LOT (Safe)
# -------------------------------------------------
@admin_bp.delete("/lot/<int:lot_id>")
def delete_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    occupied = Spot.query.filter_by(lot_id=lot_id, is_available=False).count()
    if occupied > 0:
        return jsonify({"error": "Cannot delete: some spots are occupied"}), 400

    # Safe delete
    Spot.query.filter_by(lot_id=lot_id).delete(synchronize_session=False)
    db.session.delete(lot)
    db.session.commit()

    return jsonify({"message": "Parking Lot Deleted"}), 200


# -------------------------------------------------
# TOGGLE SPOT STATUS
# -------------------------------------------------
@admin_bp.patch("/spot/<int:spot_id>/set_available")
def set_spot_available(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return jsonify({"error": "Spot Not Found"}), 404
    spot.is_available = True
    db.session.commit()
    return jsonify({"message": "Spot marked AVAILABLE"}), 200


@admin_bp.patch("/spot/<int:spot_id>/set_unavailable")
def set_spot_unavailable(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        return jsonify({"error": "Spot Not Found"}), 404

    # Prevent marking unavailable if a car is parked
    if not spot.is_available:
        return jsonify({"error": "Spot has a parked vehicle"}), 400

    spot.is_available = False
    db.session.commit()
    return jsonify({"message": "Spot marked UNAVAILABLE"}), 200


# -------------------------------------------------
# CURRENT PARKED VEHICLES
# -------------------------------------------------
@admin_bp.get("/parked")
def view_parked_vehicles():
    vehicles = Vehicle.query.filter_by(exit_time=None).all()
    out = []

    for v in vehicles:
        user = User.query.get(v.user_id)
        spot = Spot.query.get(v.spot_id)
        lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None

        out.append({
            "vehicle_id": v.id,
            "number_plate": v.number_plate,
            "user_name": user.name if user else "Unknown",
            "lot_name": lot.name if lot else None,
            "spot_number": spot.spot_number if spot else None,
            "entry_time": v.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Parked"
        })

    return jsonify(out), 200

@admin_bp.get("/lot/<int:lot_id>/spot-status")
def lot_spot_status(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    spots = []
    for s in lot.spots:
        vehicle = Vehicle.query.filter_by(spot_id=s.id, exit_time=None).first()
        user = User.query.get(vehicle.user_id) if vehicle else None
        spots.append({
            "spot_id": s.id,
            "spot_number": s.spot_number,
            "is_available": s.is_available,
            "vehicle_number": vehicle.number_plate if vehicle else None,
            "user_name": user.name if user else None,
            "entry_time": vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S") if vehicle else None,
        })

    return jsonify({
        "lot_id": lot.id,
        "lot_name": lot.name,
        "spots": spots
    }), 200

@admin_bp.get("/users")
def get_all_users():
    users = User.query.filter_by(is_admin=False).all()
    data = []
    for u in users:
        total_sessions = Vehicle.query.filter_by(user_id=u.id).count()
        last_vehicle = (
            Vehicle.query.filter_by(user_id=u.id)
            .order_by(Vehicle.entry_time.desc())
            .first()
        )
        last_seen = last_vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S") if last_vehicle else None

        data.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "total_sessions": total_sessions,
            "last_activity": last_seen,
        })

    return jsonify({"users": data}), 200

@admin_bp.get("/summary")
def admin_summary():
    lots = ParkingLot.query.all()
    lot_data = []

    for lot in lots:
        total_spots = len(lot.spots)
        available = sum(1 for s in lot.spots if s.is_available)
        occupied = total_spots - available
        revenue = 0.0

        vehicles = Vehicle.query.filter_by(lot_id=lot.id).all()
        for v in vehicles:
            if v.exit_time and v.entry_time:
                hours = (v.exit_time - v.entry_time).total_seconds() / 3600
                revenue += round(round(hours, 2) * lot.price, 2)

        lot_data.append({
            "lot_id": lot.id,
            "name": lot.name,
            "total_spots": total_spots,
            "occupied_spots": occupied,
            "available_spots": available,
            "total_revenue": round(revenue, 2),
        })

    return jsonify({"lots": lot_data}), 200
