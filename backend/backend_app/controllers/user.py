from flask import Blueprint, request, jsonify, make_response, current_app
from backend_app import db, cache
from backend_app.models import User, ParkingLot, Spot, Vehicle
from datetime import datetime
from celery.result import AsyncResult
import math, csv, io

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")

def compute_hours_and_cost(entry_time, exit_time, price_per_hour):
    if not entry_time:
        return 0, 0
    if not exit_time:
        exit_time = datetime.utcnow()

    seconds = (exit_time - entry_time).total_seconds()
    seconds = max(0, seconds)
    hours = math.ceil(seconds / 3600)
    hours = max(1, hours)
    cost = hours * float(price_per_hour or 0)
    return hours, cost

def vehicle_to_record(v):
    lot = ParkingLot.query.get(getattr(v, "lot_id", None))
    spot = Spot.query.get(getattr(v, "spot_id", None))

    record = {
        "vehicle_id": v.id,
        "number_plate": v.number_plate,
        "lot_id": lot.id if lot else None,
        "lot_name": lot.name if lot else None,
        "spot_id": spot.id if spot else None,
        "spot_number": spot.spot_number if spot else None,
        "entry_time": v.entry_time.strftime("%Y-%m-%d %H:%M:%S") if v.entry_time else None,
        "exit_time": v.exit_time.strftime("%Y-%m-%d %H:%M:%S") if v.exit_time else None,
    }

    if v.entry_time:
        if v.exit_time and lot:
            hours, cost = compute_hours_and_cost(v.entry_time, v.exit_time, lot.price)
            record["hours"] = hours
            record["cost"] = cost
        elif lot:
            hours, cost = compute_hours_and_cost(v.entry_time, None, lot.price)
            record["provisional_hours"] = hours
            record["provisional_cost"] = cost

    return record

@cache.cached(timeout=20, key_prefix="public_lots")
def get_all_lots_cached():
    lots = ParkingLot.query.all()
    output = []
    for lot in lots:
        output.append({
            "lot_id": lot.id,
            "name": lot.name,
            "location": lot.location,
            "price": lot.price,
            "available_spots": sum(1 for s in lot.spots if getattr(s, "is_available", True)),
            "total_spots": len(lot.spots)
        })
    return output

def clear_cache_safely():
    try:
        cache.clear()
    except Exception:
        pass

@user_bp.post("/register")
def register_user():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "All fields required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    clear_cache_safely()

    return jsonify({
        "message": "User Registered Successfully!",
        "user_id": user.id
    }), 201

@user_bp.post("/login")
def login_user():
    data = request.get_json(force=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email & Password required"}), 400

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Invalid Email or Password"}), 401

    return jsonify({
        "message": "Login Successful!",
        "role": "user",
        "user_id": user.id,
        "redirect": "/user/dashboard"
    }), 200

@user_bp.get("/dashboard/<int:user_id>")
def user_dashboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    active_vehicles = Vehicle.query.filter_by(
        user_id=user_id,
        exit_time=None
    ).all()

    active_list = []
    for v in active_vehicles:
        spot = Spot.query.get(v.spot_id)
        lot = ParkingLot.query.get(v.lot_id)
        active_list.append({
            "vehicle_id": v.id,
            "number_plate": v.number_plate,
            "lot_name": lot.name if lot else None,
            "spot_number": spot.spot_number if spot else None,
            "entry_time": v.entry_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    lots_data = get_all_lots_cached()

    return jsonify({
        "message": "User Dashboard Data",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "active_parkings": active_list,
        "parking_lots": lots_data
    }), 200

@user_bp.post("/park")
def park_vehicle():
    data = request.get_json(force=True) or {}

    user_id = data.get("user_id")
    vehicle_number = data.get("vehicle_number")
    lot_id = data.get("lot_id")

    if not all([user_id, vehicle_number, lot_id]):
        return jsonify({"error": "All fields required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking Lot Not Found"}), 404

    spot = Spot.query.filter_by(lot_id=lot_id, is_available=True).order_by(Spot.spot_number.asc()).first()
    if not spot:
        return jsonify({"error": "Parking Lot Full"}), 400

    vehicle = Vehicle(
        number_plate=vehicle_number,
        user_id=user_id,
        spot_id=spot.id,
        lot_id=lot_id,
        entry_time=datetime.utcnow()
    )

    db.session.add(vehicle)
    spot.is_available = False
    db.session.commit()
    clear_cache_safely()

    return jsonify({
        "message": "Vehicle Parked Successfully!",
        "spot_number": spot.spot_number,
        "vehicle_id": vehicle.id
    }), 201

@user_bp.patch("/unpark/<int:vehicle_id>")
def unpark_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle Not Found"}), 404

    if vehicle.exit_time:
        return jsonify({"error": "Vehicle already unparked"}), 400

    spot = Spot.query.get(getattr(vehicle, "spot_id", None))
    lot = ParkingLot.query.get(getattr(vehicle, "lot_id", None))

    if spot:
        spot.is_available = True

    vehicle.exit_time = datetime.utcnow()
    hours, cost = compute_hours_and_cost(vehicle.entry_time, vehicle.exit_time, lot.price if lot else 0)

    if hasattr(vehicle, "cost"):
        vehicle.cost = cost

    db.session.commit()
    clear_cache_safely()

    return jsonify({
        "message": "Vehicle Unparked Successfully!",
        "spot_freed": spot.spot_number if spot else None,
        "exit_time": vehicle.exit_time.strftime("%Y-%m-%d %H:%M:%S"),
        "hours": hours,
        "cost": cost
    }), 200

@user_bp.get("/history/<int:user_id>")
def user_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    vehicles = Vehicle.query.filter_by(user_id=user_id).order_by(Vehicle.entry_time.desc()).all()
    history = [vehicle_to_record(v) for v in vehicles]

    return jsonify({
        "message": "User Parking History",
        "history": history
    }), 200

@user_bp.get("/summary/<int:user_id>")
def user_summary(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    total_spent = 0
    sessions = 0
    lot_usage = {}

    for v in vehicles:
        lot = ParkingLot.query.get(getattr(v, "lot_id", None))
        if v.exit_time and lot:
            _, cost = compute_hours_and_cost(v.entry_time, v.exit_time, lot.price)
            total_spent += cost
            sessions += 1
            lot_usage[lot.id] = lot_usage.get(lot.id, 0) + 1

    most_used = None
    if lot_usage:
        most_used_id = max(lot_usage, key=lot_usage.get)
        lot_obj = ParkingLot.query.get(most_used_id)
        most_used = {
            "lot_id": lot_obj.id,
            "name": lot_obj.name,
            "uses": lot_usage[most_used_id]
        }

    return jsonify({
        "message": "User Summary",
        "stats": {
            "total_spent": total_spent,
            "total_sessions": sessions,
            "most_used_lot": most_used
        }
    }), 200

@user_bp.get("/export/history/<int:user_id>")
def export_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    task = current_app.celery.send_task("export_user_history", args=[user_id])

    return jsonify({
        "message": "Your export is being prepared!",
        "task_id": task.id,
        "status": "processing"
    }), 202

@user_bp.get("/export/result/<task_id>")
def download_export(task_id):
    result = current_app.celery.AsyncResult(task_id)
    if not result.ready():
        return jsonify({"status": "processing"}), 202

    csv_data = result.get()
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=history.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@user_bp.get("/export/status/<task_id>")
def export_status(task_id):
    result = AsyncResult(task_id, app=current_app.celery)
    return jsonify({
        "task_id": task_id,
        "status": result.status,
        "state": result.state
    }), 200

@user_bp.get("/monthly-summary/<int:user_id>")
def monthly_summary(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    now = datetime.utcnow()
    if now.month == 1:
        month = 12
        year = now.year - 1
    else:
        month = now.month - 1
        year = now.year

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    q = (
        Vehicle.query
        .filter(Vehicle.user_id == user_id)
        .filter(Vehicle.entry_time >= start_date)
        .filter(Vehicle.entry_time < end_date)
    )
    vehicles = q.all()

    total_sessions = len(vehicles)
    total_amount = 0.0
    lot_count = {}
    recent = []

    for v in vehicles:
        lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None
        if lot:
            lot_count[lot.name] = lot_count.get(lot.name, 0) + 1

        if v.exit_time and v.entry_time and lot:
            hours = (v.exit_time - v.entry_time).total_seconds() / 3600
            hours_rounded = round(hours, 2)
            total_amount += round(hours_rounded * lot.price, 2)

        recent.append({
            "id": v.id,
            "number_plate": v.number_plate,
            "lot_name": lot.name if lot else "",
            "entry_time": v.entry_time.strftime("%Y-%m-%d %H:%M") if v.entry_time else "",
            "exit_time": v.exit_time.strftime("%Y-%m-%d %H:%M") if v.exit_time else "",
        })

    recent = recent[:10]
    most_used_lot = None
    if lot_count:
        most_used_lot = max(lot_count.items(), key=lambda x: x[1])[0]

    month_label = start_date.strftime("%B %Y")

    return jsonify({
        "month": month_label,
        "total_sessions": total_sessions,
        "total_amount": round(total_amount, 2),
        "most_used_lot": most_used_lot or "N/A",
        "recent_activity": recent,
    }), 200
