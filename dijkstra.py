import heapq

INF = 1e9

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, distance, cost):
        if source not in self.graph:
            self.graph[source] = {}
        if destination not in self.graph:
            self.graph[destination] = {}

        weight = 0.6 * distance + 0.4 * cost

        self.graph[source][destination] = {
            "distance": distance,
            "cost": cost,
            "weight": weight
        }

        self.graph[destination][source] = {
            "distance": distance,
            "cost": cost,
            "weight": weight
        }


def dijkstra_algorithm(graph_obj, start, end):
    graph = graph_obj.graph
    dist = {node: INF for node in graph}
    prev = {node: None for node in graph}

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)

        if node == end:
            break

        for neighbor in graph[node]:
            edge = graph[node][neighbor]
            new_dist = current_dist + edge["weight"]

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = prev[current]

    path.reverse()

    total_distance = 0
    total_cost = 0

    for i in range(len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        total_distance += edge["distance"]
        total_cost += edge["cost"]

    return path, total_distance, total_cost