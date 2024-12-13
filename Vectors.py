import heapq
import os
from copy import deepcopy
from collections import defaultdict

# Function to parse the input file
def parse_input_file(file_path):
    initial_edges = defaultdict(list)
    time_changes = defaultdict(list)

    with open(file_path, 'r') as file:
        for line in file:
            if ': ' not in line:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            try:
                time, data = line.strip().split(': ')
                time = int(time)
                u, v, cost = data.split(', ')
                u, v = u.strip(), v.strip()
                cost = int(cost)
                if time == 0:
                    initial_edges[u].append((v, cost))
                    initial_edges[v].append((u, cost))  
                else:
                    time_changes[time].append((u, v, cost))
            except ValueError as e:
                print(f"Error parsing line '{line.strip()}': {e}")
                continue
    return initial_edges, time_changes

# Function to perform Dijkstra's algorithm for SPF
def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[source] = 0
    pq = [(0, source)]  # Priority queue

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes

# Distance Vector Algorithm with consistent step count
def distance_vector(graph, time_changes, max_steps=100, stability_threshold=3):
    nodes = list(graph.keys())
    history = []  
    next_hops = {node: {dest: None for dest in nodes} for node in nodes}
    local_vectors = {node: {dest: float('inf') for dest in nodes} for node in nodes}
    
    # Initialize self-costs 
    for node in nodes:
        local_vectors[node][node] = 0

    total_steps = 0  

    for current_time in sorted([0] + list(time_changes.keys())):
        # Create a copy of the graph at the current time step
        dv_graph = deepcopy(graph)
        if current_time > 0:
            apply_time_changes(dv_graph, time_changes, current_time)

        updated = True
        stable_iterations = 0
        previous_vectors = deepcopy(local_vectors)

        while stable_iterations < stability_threshold and total_steps < max_steps:
            updated = False
            total_steps += 1  

            # For each node, update its distance vector
            for node in nodes:
                for neighbor, cost in dv_graph[node]: 
                    for dest in nodes:
                        if local_vectors[neighbor][dest] < float('inf'):
                            new_cost = cost + local_vectors[neighbor][dest]
                            if new_cost < local_vectors[node][dest]:
                                local_vectors[node][dest] = new_cost
                                next_hops[node][dest] = neighbor
                                updated = True

            # Check for stability
            if local_vectors == previous_vectors:
                stable_iterations += 1
            else:
                stable_iterations = 0

            previous_vectors = deepcopy(local_vectors)

            
            history.append((current_time, total_steps, deepcopy(local_vectors)))

            # Stop if stable for the required threshold
            if not updated and stable_iterations >= stability_threshold:
                break

    return history, next_hops, local_vectors

# Function to apply graph updates based on time changes
def apply_time_changes(graph, time_changes, current_time):
    if current_time in time_changes:
        for u, v, cost in time_changes[current_time]:
            for i, (neighbor, weight) in enumerate(graph[u]):
                if neighbor == v:
                    graph[u][i] = (v, cost)
                    break
            else:
                graph[u].append((v, cost))
            for i, (neighbor, weight) in enumerate(graph[v]):
                if neighbor == u:
                    graph[v][i] = (u, cost)
                    break
            else:
                graph[v].append((u, cost))

# Function to write SPF results
def write_spf_results(input_file, spf_results):
    base_name = os.path.splitext(input_file)[0]

    for node, results in spf_results.items():
        with open(f"{base_name}_SPF_{node}.txt", "w") as file:
            file.write(f"Steps\tDestination\tCost\tPath\n")
            for step, (distances, paths) in results.items():
                for dest, cost in distances.items():
                    path = []
                    current = dest
                    while current:
                        path.append(current)
                        current = paths[current]
                    path.reverse()
                    file.write(f"{step}\t{dest}\t{cost}\t{' -> '.join(path)}\n")

# Function to write Distance Vector results with Local Distance Vector
def write_distance_vector_output(input_file, dv_history, next_hops):
    base_name = os.path.splitext(input_file)[0]

    for node in next_hops.keys():
        with open(f"{base_name}_DVA_{node}.txt", "w") as file:
            file.write(f"Timestep\tDestination\tNextHop\tOverallCost\tLocal Distance Vector\n")
            
            for time, step, vectors in dv_history:
                current_vector = vectors[node]  

                
                local_vector_str = " | " + " ".join(
                    str(int(current_vector[dest])) if current_vector[dest] != float('inf') else "N"
                    for dest in current_vector
                )

                # Write routing table entries 
                for dest, cost in current_vector.items():
                    nexthop = next_hops[node].get(dest, None)
                    cost_str = str(int(cost)) if cost != float('inf') else "N"
                    nexthop_str = nexthop if nexthop else "N"
                    file.write(f"{time}\t{dest}\t{nexthop_str}\t{cost_str}\t{local_vector_str}\n")

# Main function
def main(input_file):
    initial_graph, time_changes = parse_input_file(input_file)

    graph_spf = deepcopy(initial_graph)
    graph_dv = deepcopy(initial_graph)

    # SPF results
    spf_results = {node: {} for node in graph_spf.keys()}
    for time in sorted([0] + list(time_changes.keys())):
        if time > 0:
            apply_time_changes(graph_spf, time_changes, time)
        for node in graph_spf.keys():
            distances, paths = dijkstra(graph_spf, node)
            spf_results[node][time] = (distances, paths)

    # Distance Vector Algorithm
    dv_history, next_hops, _ = distance_vector(graph_dv, time_changes)

    # Write outputs
    write_spf_results(input_file, spf_results)
    write_distance_vector_output(input_file, dv_history, next_hops)

# Entry point
if __name__ == "__main__":
    input_file = "topology.txt"  # Replace with your input file
    main(input_file)
