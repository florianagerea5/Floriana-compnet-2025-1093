from heapq import heappop, heappush

def dijkstra(graph, source):
  """
  Implements Dijkstra's algorithm to find shortest paths from a source vertex in a weighted graph.

  Args:
      graph: A dictionary representing the graph. Keys are vertices, values are dictionaries
             with neighbors as keys and edge weights as values.
      source: The starting vertex for the shortest path search.

  Returns:
      A dictionary containing the distance to each vertex from the source and the predecessor
      vertex in the shortest path (for path reconstruction). None if there are negative edges.
  """
  # Initialize distances to infinity (except source) and predecessors to None
  distances = {vertex: float('inf') for vertex in graph}
  distances[source] = 0
  predecessors = {vertex: None for vertex in graph}

  # Use a priority queue (min-heap) to prioritize exploring vertices with lower tentative distances
  pq = [(0, source)]

  print('DISTANCES')
  print(distances)
  print('PREDECESSORS')
  print(predecessors)
  print('QUEUE')
  print(pq)

  # Relaxation process
  while pq:
    current_distance, current_vertex = heappop(pq)
    print(f'popping {current_vertex}')
    
    # Check for negative edge weights (Dijkstra doesn't work with them)
    # if current_distance < distances[current_vertex]:
    #   return None  # Negative weight detected

    # Relaxation for neighbors
    for neighbor, weight in graph[current_vertex].items():
      new_distance = current_distance + weight
      if new_distance < distances[neighbor]:
        distances[neighbor] = new_distance
        predecessors[neighbor] = current_vertex
        heappush(pq, (new_distance, neighbor))
      print('DISTANCES')
      print(distances)
      print('PREDECESSORS')
      print(predecessors)
      print('QUEUE')
      print(pq)

  return distances, predecessors

# Example usage
graph = {
  'A': {'B': 4, 'C': 2},
  'B': {'D': 2, 'E': 3, 'A': 4},
  'C': {'D': 3, 'E': 1, 'A': 2},
  'D': {'C': 3, 'B': 2},
  'E': {'B': 3, 'C': 1},
}

source = 'C'

distances, predecessors = dijkstra(graph, source)  # copy to avoid modifying original graph

if distances is None:
  print("Error: Negative edges detected in graph")
else:
  # Print shortest distances
  print("Shortest distances from", source)
  for vertex, distance in distances.items():
    print(vertex, ":", distance)

  # Print shortest path for a specific destination (if desired)
  # destination = 'E'
  # path = []
  # while destination != source:
  #   path.append(destination)
  #   destination = predecessors[destination]
  # path.append(source)
  # print("Shortest path to", destination, ": -> ".join(path[::-1]))
