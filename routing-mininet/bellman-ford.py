# notes
# https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/

def bellman_ford(graph, source):
  """
  Implements the Bellman-Ford algorithm to find shortest paths from a source vertex.

  Args:
      graph: A dictionary representing the graph. Keys are vertices, values are dictionaries
             with neighbors as keys and edge weights as values.
      source: The starting vertex for the shortest path search.

  Returns:
      A dictionary containing the distance to each vertex from the source and the predecessor
      vertex in the shortest path (for path reconstruction). None if a negative cycle is detected.
  """
  # Initialize distances to infinity (except source) and predecessors to None
  distances = {vertex: float('inf') for vertex in graph}
  distances[source] = 0
  predecessors = {vertex: None for vertex in graph}
 
  print('INITIAL')
  print('DISTANCES')
  print(distances)
  print('PREDECESSORS')
  print(predecessors)
  # Relax edges |V|-1 times (Bellman-Ford property)
  for i in range(len(graph) - 1):
    for vertex, neighbors in graph.items():
      for neighbor, weight in neighbors.items():
        new_distance = distances[vertex] + weight
        if new_distance < distances[neighbor]:
          distances[neighbor] = new_distance
          predecessors[neighbor] = vertex    
    print(f'ITERATION {i}')
    print('DISTANCES')
    print(distances)
    print('PREDECESSORS')
    print(predecessors)

  # Check for negative-weight cycles (relax one more time)
  for vertex, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
      new_distance = distances[vertex] + weight
      if new_distance < distances[neighbor]:
        return None  # Negative cycle detected

  return distances, predecessors

# Example usage
graph = {
  'A': {'B': 4, 'C': 2},
  'B': {'D': 2, 'E': 3, 'A': 4},
  'C': {'D': 3, 'E': 1, 'A': 2},
  'D': {'C': 3, 'B': 2},
  'E': {'B': 3, 'C': 1},
}

source = 'D'

distances, predecessors = bellman_ford(graph, source)

if distances is None:
  print("Error: Negative cycle detected")
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
