from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from dijkstra import Graph, dijkstra_algorithm
from extensions import db
import os
from dotenv import load_dotenv

load_dotenv()
def create_app():
    app = Flask(__name__)
    # Load configuration from .env file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

    # Initialize the app with the extension
    db.init_app(app)

    # Import models here to avoid circular imports
    from models import Station, Route, Booking

    @app.route('/')
    def index():
        stations = Station.query.all()
        return render_template('index.html', stations=stations)

    @app.route('/find_route', methods=['POST'])
    def find_route():
        try:
            source_id = int(request.form.get('source'))
            destination_id = int(request.form.get('destination'))
            
            # Validate station IDs
            source = Station.query.get(source_id)
            destination = Station.query.get(destination_id)
            
            if not source or not destination:
                flash('Invalid station selection. Please select valid stations.')
                return redirect(url_for('index'))
            
            if source_id == destination_id:
                flash('Source and destination cannot be the same.')
                return redirect(url_for('index'))
            
            # Create graph and find route
            graph = Graph()
            routes = Route.query.all()
            
            # Add all routes to the graph
            for route in routes:
                graph.add_edge(route.source_id, route.destination_id, route.distance, route.cost)
            
            # Check if both stations exist in the graph
            if source_id not in graph.graph or destination_id not in graph.graph:
                flash('No route available between these stations.')
                return redirect(url_for('index'))
            
            # Find the route
            path, total_distance, total_cost = dijkstra_algorithm(graph, source_id, destination_id)
            
            if not path:
                flash('No route found between these stations.')
                return redirect(url_for('index'))
            
            # Calculate segment distances and costs
            segment_distances = []
            segment_costs = []
            
            for i in range(len(path) - 1):
                current_station = path[i]
                next_station = path[i + 1]
                
                # Find the route between these stations
                route = Route.query.filter_by(
                    source_id=current_station,
                    destination_id=next_station
                ).first()
                
                if route:
                    segment_distances.append(route.distance)
                    segment_costs.append(route.cost)
            
            # Store the route in the session
            session['path'] = path
            session['segment_distances'] = segment_distances
            session['segment_costs'] = segment_costs
            session['total_distance'] = total_distance
            session['total_cost'] = total_cost
            
            return render_template('result.html', 
                                 path=path,
                                 total_distance=total_distance,
                                 total_cost=total_cost,
                                 source=source,
                                 destination=destination)
                                 
        except (ValueError, TypeError):
            flash('Invalid input. Please select valid stations.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))

    @app.route('/book', methods=['POST'])
    def book():
        try:
            # Get form data with validation
            name = request.form.get('name')
            email = request.form.get('email')
            travel_date_str = request.form.get('travel_date')
            source_id = request.form.get('source')
            destination_id = request.form.get('destination')
            
            # Validate required fields
            if not all([name, email, travel_date_str, source_id, destination_id]):
                flash('All fields are required', 'error')
                return redirect(url_for('index'))
            
            try:
                travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
                source_id = int(source_id)
                destination_id = int(destination_id)
            except ValueError:
                flash('Invalid date or station selection', 'error')
                return redirect(url_for('index'))
            
            # Get the path and costs from the session
            path = session.get('path', [])
            segment_distances = session.get('segment_distances', [])
            segment_costs = session.get('segment_costs', [])
            total_distance = session.get('total_distance', 0)
            total_cost = session.get('total_cost', 0)
            
            if not path:
                flash('Please find a route first before booking', 'error')
                return redirect(url_for('index'))
            
            # Validate stations exist
            source = Station.query.get(source_id)
            destination = Station.query.get(destination_id)
            
            if not source or not destination:
                flash('Invalid station selection', 'error')
                return redirect(url_for('index'))
            
            # Get all stations in the path
            stations_in_path = Station.query.filter(Station.id.in_(path)).all()
            station_dict = {station.id: station for station in stations_in_path}
            
            # Create new booking
            booking = Booking(
                name=name,
                email=email,
                travel_date=travel_date,
                source_id=source_id,
                destination_id=destination_id,
                path=','.join(map(str, path)),
                total_distance=total_distance,
                total_cost=total_cost
            )
            
            db.session.add(booking)
            db.session.commit()
            
            return render_template('booking_confirmation.html',
                                 booking=booking,
                                 source=source,
                                 destination=destination,
                                 path=path,
                                 stations=station_dict,
                                 segment_distances=segment_distances,
                                 segment_costs=segment_costs,
                                 total_distance=total_distance,
                                 total_cost=total_cost)
                                 
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating booking: {str(e)}', 'error')
            return redirect(url_for('index'))

    @app.route('/algorithm')
    def algorithm():
        return render_template('algorithm.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True) 