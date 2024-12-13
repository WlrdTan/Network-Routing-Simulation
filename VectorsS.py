import heapq
import os
from copy import deepcopy
from collections import defaultdict

# Function to parse the input file with no spacing
def parse_input_file(file_path):
    initial_edges = defaultdict(list)
    time_changes = defaultdict(list)

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove any leading/trailing spaces
            if not line:
                print(f"Skipping invalid line: {line}")
                continue

            # Normalize the line 
            try:
                if ':' in line:
                    time, data = line.split(':', 1) 
                    time = int(time.strip())
                    u, v, cost = map(str.strip, data.split(','))
                    cost = int(cost)

                    if time == 0:
                        initial_edges[u].append((v, cost))
                        initial_edges[v].append((u, cost))  # Undirected graph
                    else:
                        time_changes[time].append((u, v, cost))
                else:
                    print(f"Skipping invalid line: {line}")
            except ValueError as e:
                print(f"Error parsing line '{line}': {e}")
                continue

    return initial_edges, time_changes

# Dijkstra's algorithm 
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

# Distance Vector Algorithm
def distance_vector(graph, time_changes, max_steps=100, stability_threshold=3):
    nodes = list(graph.keys())
    history = []
    next_hops = {node: {dest: None for dest in nodes} for node in nodes}

    total_steps = 0

    for current_time in sorted([0] + list(time_changes.keys())):
        dv_graph = deepcopy(graph)
        if current_time > 0:
            apply_time_changes(dv_graph, time_changes, current_time)

        routing_tables = {node: {dest: float('inf') for dest in nodes} for node in nodes}
        for node in nodes:
            routing_tables[node][node] = 0

        updated = True
        stable_iterations = 0
        previous_tables = None

        while stable_iterations < stability_threshold and total_steps < max_steps:
            updated = False
            total_steps += 1

            current_tables = {node: dict(routing_tables[node]) for node in nodes}

            for node in nodes:
                for neighbor, cost in dv_graph[node]:
                    for dest in nodes:
                        if routing_tables[neighbor][dest] < float('inf'):
                            new_cost = cost + routing_tables[neighbor][dest]
                            if new_cost < routing_tables[node][dest]:
                                routing_tables[node][dest] = new_cost
                                next_hops[node][dest] = neighbor
                                updated = True

            if previous_tables == current_tables:
                stable_iterations += 1
            else:
                stable_iterations = 0

            previous_tables = current_tables
            history.append((current_time, total_steps, {node: dict(routing_tables[node]) for node in nodes}))

            if not updated and stable_iterations >= stability_threshold:
                break

    return history, next_hops

# Function to apply graph updates
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

# Function to write DV results
def write_distance_vector_output(input_file, dv_history, next_hops):
    base_name = os.path.splitext(input_file)[0]

    for node in next_hops.keys():
        with open(f"{base_name}_DVA_{node}.txt", "w") as file:
            file.write(f"Timestep\tDestination\tNext Hop\tOverall Cost\tLocal Distance Vector\n")
            for time, step, states in dv_history:
                table = states[node]
                local_vector = " | " + " ".join(
                    str(int(table[dest])) if table[dest] != float('inf') else "N" for dest in table
                )

                for dest, cost in table.items():
                    nexthop = next_hops[node].get(dest, None)
                    cost_str = str(int(cost)) if cost != float('inf') else "N"
                    nexthop_str = nexthop if nexthop else "N"
                    file.write(f"{time}\t{dest}\t{nexthop_str}\t{cost_str}\t{local_vector}\n")

# Main function
def main(input_file):
    initial_graph, time_changes = parse_input_file(input_file)

    graph_spf = deepcopy(initial_graph)
    graph_dv = deepcopy(initial_graph)

    spf_results = {node: {} for node in graph_spf.keys()}
    for time in sorted([0] + list(time_changes.keys())):
        if time > 0:
            apply_time_changes(graph_spf, time_changes, time)
        for node in graph_spf.keys():
            distances, paths = dijkstra(graph_spf, node)
            spf_results[node][time] = (distances, paths)

    dv_history, next_hops = distance_vector(graph_dv, time_changes)

    write_spf_results(input_file, spf_results)
    write_distance_vector_output(input_file, dv_history, next_hops)

if __name__ == "__main__":
    input_file = "topology.txt"  # Replace with your input file
    main(input_file)
