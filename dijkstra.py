import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = {}
        
    def add_edge(self, source, destination, distance, cost):
        if source not in self.graph:
            self.graph[source] = {}
        if destination not in self.graph:
            self.graph[destination] = {}
            
        # Add edge in both directions
        self.graph[source][destination] = {'distance': distance, 'cost': cost}
        self.graph[destination][source] = {'distance': distance, 'cost': cost}

def dijkstra_algorithm(graph, start, end):
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Start and end must be integers")
    
    if start not in graph.graph or end not in graph.graph:
        return [], 0, 0
    
    # Initialize distances and previous nodes
    distances = {node: float('infinity') for node in graph.graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.graph}
    unvisited = set(graph.graph.keys())
    
    while unvisited:
        # Find the unvisited node with the smallest distance
        current = min(unvisited, key=lambda node: distances[node])
        
        # If we've reached the end node, we can stop
        if current == end:
            break
            
        # Remove current node from unvisited set
        unvisited.remove(current)
        
        # If current node is unreachable, skip it
        if distances[current] == float('infinity'):
            continue
            
        # Check all neighbors of current node
        for neighbor, edge_data in graph.graph[current].items():
            if neighbor not in unvisited:
                continue
                
            # Calculate new distance (considering both distance and cost)
            distance = edge_data['distance']
            cost = edge_data['cost']
            weight = distance + (cost * 0.1)  # Weighted combination of distance and cost
            
            new_distance = distances[current] + weight
            
            # If we found a shorter path, update it
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current
    
    # Reconstruct the path
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    # Reverse the path to get it from start to end
    path.reverse()
    
    # Calculate total distance and cost
    total_distance = 0
    total_cost = 0
    
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        edge_data = graph.graph[current][next_node]
        total_distance += edge_data['distance']
        total_cost += edge_data['cost']
    
    return path, total_distance, total_cost 