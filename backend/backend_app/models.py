from backend_app.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    # One user has many vehicles
    vehicles = db.relationship(
        "Vehicle",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.id} - {self.email}>"



class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False, index=True)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, default=0.0)

    max_spots = db.Column(db.Integer, default=0)

    # One lot has many spots
    spots = db.relationship(
        "Spot",
        backref="lot",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Optional link: retrieve all vehicles parked in lot
    vehicles = db.relationship(
        "Vehicle",
        backref="lot",
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Lot {self.id} - {self.name}>"



class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    spot_number = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)

    # One spot can have multiple vehicles over time
    vehicles = db.relationship(
        "Vehicle",
        backref="spot",
        lazy=True,
        cascade="all, delete-orphan"
    )

    
    __table_args__ = (
        db.UniqueConstraint('lot_id', 'spot_number', name='unique_spot_per_lot'),
    )

    def __repr__(self):
        return f"<Spot {self.id} - #{self.spot_number}>"



class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    number_plate = db.Column(db.String(50), unique=True, nullable=False, index=True)

    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)

    cost = db.Column(db.Float, default=0.0)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("spot.id"), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)

    def __repr__(self):
        return f"<Vehicle {self.id} - {self.number_plate}>"