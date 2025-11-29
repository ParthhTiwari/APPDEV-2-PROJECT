
import csv
import io
from datetime import datetime, timedelta
from backend_app.celery import celery_app as celery
from backend_app import db
from backend_app.models import Vehicle, ParkingLot, Spot
from backend_app.models import User   # <- import add karo
from backend_app.email_utils import send_email
from sqlalchemy import func
# ---------- EXPORT USER HISTORY TASK ----------
def compute_hours_and_cost(entry, exit, price):
    hours = (exit - entry).total_seconds() / 3600
    hours_rounded = round(hours, 2)
    cost = round(hours_rounded * price, 2)
    return hours_rounded, cost


@celery.task(name="export_user_history")
def export_user_history(user_id):
    vehicles = (
        Vehicle.query.filter_by(user_id=user_id)
        .order_by(Vehicle.entry_time.asc())
        .all()
    )

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(
        [
            "vehicle_id",
            "number_plate",
            "lot_id",
            "lot_name",
            "spot_id",
            "spot_number",
            "entry_time",
            "exit_time",
            "hours",
            "cost",
        ]
    )

    for v in vehicles:
        lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None
        spot = Spot.query.get(v.spot_id) if v.spot_id else None

        hours = ""
        cost = ""
        if v.exit_time and v.entry_time and lot:
            hours, cost = compute_hours_and_cost(
                v.entry_time, v.exit_time, lot.price
            )

        writer.writerow(
            [
                v.id,
                v.number_plate,
                lot.id if lot else "",
                lot.name if lot else "",
                spot.id if spot else "",
                spot.spot_number if spot else "",
                v.entry_time.strftime("%Y-%m-%d %H:%M:%S")
                if v.entry_time
                else "",
                v.exit_time.strftime("%Y-%m-%d %H:%M:%S")
                if v.exit_time
                else "",
                hours,
                cost,
            ]
        )

    return buffer.getvalue()


# ---------- DAILY REMINDER TASK ----------

@celery.task(name="send_daily_reminders")
def send_daily_reminders():
    """
    Roz ek baar chalne wala task.
    Jis user ne last 3 din me parking nahi ki, unko reminder email bhejta hai.
    """
    three_days_ago = datetime.utcnow() - timedelta(days=3)

    # Har user ka last parking time nikalne ke liye LEFT OUTER JOIN style query
    # Agar user ne kabhi park nahi kiya ho to last_time None rahega.
    from backend_app.models import User, Vehicle  # local import to avoid circular

    users = (
        db.session.query(
            User,
            func.max(Vehicle.entry_time).label("last_time")
        )
        .outerjoin(Vehicle, Vehicle.user_id == User.id)
        .group_by(User.id)
        .all()
    )

    for user, last_time in users:
        # admin ko skip karte hain
        if getattr(user, "is_admin", False):
            continue

        needs_reminder = False
        if last_time is None:
            # user ne kabhi park nahi kiya
            needs_reminder = True
        elif last_time < three_days_ago:
            needs_reminder = True

        if not needs_reminder:
            continue

        html = f"""
        <h3>Hello {user.name},</h3>
        <p>We noticed that you haven't used the parking app recently.</p>
        <p>If you need a parking spot, you can log in and book one easily from your dashboard.</p>
        <p>Regards,<br>Parking App</p>
        """

        try:
            send_email(
                to_email=user.email,
                subject="Parking Reminder",
                html_body=html,
            )
        except Exception:
            # real app me yahan logging karein
            continue


# ---------- MONTHLY REPORT TASK ----------

@celery.task(name="send_monthly_reports")
def send_monthly_reports():
    """
    Har mahine ke pehle din chalne wala task.
    Har user ke liye pichhle mahine ka simple HTML report mail karta hai.
    """
    from backend_app.models import User, Vehicle, ParkingLot  # local imports

    now = datetime.utcnow()
    # previous month nikalna (simple version)
    if now.month == 1:
        month = 12
        year = now.year - 1
    else:
        month = now.month - 1
        year = now.year

    # month start = 1st, month end = next month 1st
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    users = User.query.all()

    for user in users:
        if getattr(user, "is_admin", False):
            continue

        q = (
            Vehicle.query
            .filter(Vehicle.user_id == user.id)
            .filter(Vehicle.entry_time >= start_date)
            .filter(Vehicle.entry_time < end_date)
        )

        vehicles = q.all()
        if not vehicles:
            # koi activity nahi, mail skip kar sakte ho; ya phir "No activity" report bhejo
            continue

        total_sessions = len(vehicles)
        total_amount = 0.0
        lot_count = {}

        for v in vehicles:
            lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None
            if lot:
                lot_count[lot.name] = lot_count.get(lot.name, 0) + 1

            if v.exit_time and v.entry_time and lot:
                hours, cost = compute_hours_and_cost(v.entry_time, v.exit_time, lot.price)
                total_amount += cost

        most_used_lot = None
        if lot_count:
            most_used_lot = max(lot_count.items(), key=lambda x: x[1])[0]

        # simple HTML report
        month_label = start_date.strftime("%B %Y")
        html_rows = ""
        for v in vehicles[:10]:  # sirf first 10 rows table me dikhate hain, baaki summary
            lot = ParkingLot.query.get(v.lot_id) if v.lot_id else None
            html_rows += f"""
            <tr>
              <td>{v.number_plate}</td>
              <td>{lot.name if lot else ''}</td>
              <td>{v.entry_time.strftime('%Y-%m-%d %H:%M') if v.entry_time else ''}</td>
              <td>{v.exit_time.strftime('%Y-%m-%d %H:%M') if v.exit_time else ''}</td>
            </tr>
            """

        html = f"""
        <h2>Monthly Parking Report – {month_label}</h2>
        <p>Hello {user.name},</p>
        <p>Here is your parking summary for {month_label}.</p>
        <ul>
          <li>Total parking sessions: <b>{total_sessions}</b></li>
          <li>Total amount spent: <b>₹{round(total_amount, 2)}</b></li>
          <li>Most used parking lot: <b>{most_used_lot or 'N/A'}</b></li>
        </ul>
        <p>Recent parking activity:</p>
        <table border="1" cellpadding="4" cellspacing="0">
          <tr>
            <th>Vehicle</th>
            <th>Lot</th>
            <th>Entry Time</th>
            <th>Exit Time</th>
          </tr>
          {html_rows}
        </table>
        <p>Regards,<br>Parking App</p>
        """

        try:
            send_email(
                to_email=user.email,
                subject=f"Your Parking Report – {month_label}",
                html_body=html,
            )
        except Exception:
            continue
