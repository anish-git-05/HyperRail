from app import create_app
from models import Station, Route, db

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing data
        Route.query.delete()
        Station.query.delete()
        
        # Add stations
        stations = [
            Station(name='Mumbai Central', location='Mumbai, Maharashtra'),
            Station(name='Pune Junction', location='Pune, Maharashtra'),
            Station(name='Ahmedabad Junction', location='Ahmedabad, Gujarat'),
            Station(name='Jaipur Junction', location='Jaipur, Rajasthan'),
            Station(name='Delhi Central', location='New Delhi, Delhi')
        ]
        
        for station in stations:
            db.session.add(station)
        db.session.commit()
        
        # Add routes with distances and costs
        routes = [
            # Mumbai to Pune
            Route(source_id=1, destination_id=2, distance=150, cost=2000),
            # Mumbai to Ahmedabad
            Route(source_id=1, destination_id=3, distance=500, cost=5000),
            # Pune to Ahmedabad
            Route(source_id=2, destination_id=3, distance=600, cost=6000),
            # Ahmedabad to Jaipur
            Route(source_id=3, destination_id=4, distance=700, cost=7000),
            # Jaipur to Delhi
            Route(source_id=4, destination_id=5, distance=300, cost=3000),
            # Mumbai to Jaipur (direct)
            Route(source_id=1, destination_id=4, distance=1000, cost=10000),
            # Pune to Delhi
            Route(source_id=2, destination_id=5, distance=1200, cost=12000)
        ]
        
        for route in routes:
            db.session.add(route)
        db.session.commit()
        
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db() 