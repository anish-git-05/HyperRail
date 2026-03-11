from app import create_app
from models import Station, Route
import numpy as np

def print_adjacency_matrix():
    app = create_app()
    with app.app_context():
        # Get all stations
        stations = Station.query.order_by(Station.id).all()
        n = len(stations)
        
        # Create adjacency matrix initialized with infinity
        matrix = np.full((n, n), float('inf'))
        
        # Set diagonal to 0
        np.fill_diagonal(matrix, 0)
        
        # Get all routes
        routes = Route.query.all()
        
        # Fill the matrix with distances
        for route in routes:
            # Convert to 0-based index
            i = route.source_id - 1
            j = route.destination_id - 1
            matrix[i][j] = route.distance
            matrix[j][i] = route.distance  # Since routes are bidirectional
        
        # Print station names
        print("\nStation Names:")
        for i, station in enumerate(stations):
            print(f"{i+1}. {station.name}")
        
        # Print the matrix
        print("\nAdjacency Matrix (Distances in km):")
        print("    ", end="")
        for station in stations:
            print(f"{station.name[:4]:>8}", end="")
        print("\n")
        
        for i, station in enumerate(stations):
            print(f"{station.name[:4]:<4}", end="")
            for j in range(n):
                if matrix[i][j] == float('inf'):
                    print(f"{'∞':>8}", end="")
                else:
                    print(f"{matrix[i][j]:>8.0f}", end="")
            print()
        
        # Print route details
        print("\nDetailed Route Information:")
        print("-" * 80)
        print(f"{'From':<20} {'To':<20} {'Distance (km)':<15} {'Cost (₹)':<15}")
        print("-" * 80)
        
        for route in routes:
            source = Station.query.get(route.source_id)
            dest = Station.query.get(route.destination_id)
            print(f"{source.name:<20} {dest.name:<20} {route.distance:<15.0f} {route.cost:<15.0f}")

if __name__ == '__main__':
    print_adjacency_matrix() 