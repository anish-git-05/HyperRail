from extensions import db
from datetime import datetime

class Station(db.Model):
    """
    Station model represents each hyperloop station in the network.
    Fields:
    - id: Unique identifier for the station
    - name: Name of the station (e.g., 'Mumbai Central')
    - location: Location description (e.g., 'Mumbai, Maharashtra')
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    # Relationships to track routes where this station is either source or destination
    source_routes = db.relationship('Route', foreign_keys='Route.source_id', backref='source_station', lazy=True)
    destination_routes = db.relationship('Route', foreign_keys='Route.destination_id', backref='destination_station', lazy=True)
    
    def __repr__(self):
        return f'<Station {self.name}>'

class Route(db.Model):
    """
    Route model represents connections between stations.
    Fields:
    - id: Unique identifier for the route
    - source_id: ID of the starting station
    - destination_id: ID of the ending station
    - distance: Distance between stations in kilometers
    - cost: Cost of travel in rupees
    """
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    distance = db.Column(db.Float, nullable=False)  # in kilometers
    cost = db.Column(db.Float, nullable=False)      # in rupees
    
    # Prevent duplicate routes between the same stations
    __table_args__ = (db.UniqueConstraint('source_id', 'destination_id', name='unique_route'),)
    
    def __repr__(self):
        return f'<Route {self.source_id} to {self.destination_id}>'

class Booking(db.Model):
    """
    Booking model stores information about passenger bookings.
    Fields:
    - id: Unique booking identifier
    - name: Passenger's name
    - email: Passenger's email
    - travel_date: Date of travel
    - source_id: Starting station ID
    - destination_id: Ending station ID
    - path: Sequence of station IDs in the journey
    - total_distance: Total journey distance
    - total_cost: Total journey cost
    - booking_date: When the booking was made
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    travel_date = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    path = db.Column(db.String(500), nullable=False)  # Store path as comma-separated station IDs
    total_distance = db.Column(db.Float, nullable=False)  # in kilometers
    total_cost = db.Column(db.Float, nullable=False)      # in rupees
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships to easily access station information
    source_station = db.relationship('Station', foreign_keys=[source_id], backref='source_bookings')
    destination_station = db.relationship('Station', foreign_keys=[destination_id], backref='destination_bookings')
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.name}>' 