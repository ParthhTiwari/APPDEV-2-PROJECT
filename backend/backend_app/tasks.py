import csv
import io
from backend_app import db
from backend_app.models import Vehicle, ParkingLot, Spot
from datetime import datetime
from celery import shared_task

def compute_hours_and_cost(entry, exit, price):
    hours = (exit - entry).total_seconds() / 3600
    hours_rounded = round(hours, 2)
    cost = round(hours_rounded * price, 2)
    return hours_rounded, cost


@shared_task(name="export_user_history")
def export_user_history(user_id):
    vehicles = Vehicle.query.filter_by(user_id=user_id).order_by(Vehicle.entry_time.asc()).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow([
        "vehicle_id", "number_plate", "lot_id", "lot_name",
        "spot_id", "spot_number", "entry_time", "exit_time",
        "hours", "cost"
    ])

    for v in vehicles:
        lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None
        spot = Spot.query.get(v.spot_id) if v.spot_id else None

        hours = ""
        cost = ""
        if v.exit_time and v.entry_time and lot:
            hours, cost = compute_hours_and_cost(v.entry_time, v.exit_time, lot.price)

        writer.writerow([
            v.id,
            v.number_plate,
            lot.id if lot else "",
            lot.name if lot else "",
            spot.id if spot else "",
            spot.spot_number if spot else "",
            v.entry_time.strftime("%Y-%m-%d %H:%M:%S") if v.entry_time else "",
            v.exit_time.strftime("%Y-%m-%d %H:%M:%S") if v.exit_time else "",
            hours,
            cost
        ])

    
    return buffer.getvalue()
