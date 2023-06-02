import networkx as nx
import numpy as np
from typing import List, Tuple
import random

def bellman_ford(G: nx.DiGraph, source: int) -> np.ndarray:
    distance = np.full(len(G.nodes), np.inf)
    distance[source] = 0

    for _ in range(len(G.nodes) - 1):
        for u, v, attr in G.edges(data=True):
            weight = attr['weight']
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight

    return distance

def dijkstra(G: nx.DiGraph, source: int) -> np.ndarray:
    distance = np.full(len(G.nodes), np.inf)
    distance[source] = 0

    visited = np.zeros(len(G.nodes), dtype=bool)

    while True:
        u = -1
        min_distance = np.inf
        for v in range(len(G.nodes)):
            if not visited[v] and distance[v] < min_distance:
                min_distance = distance[v]
                u = v

        if u == -1:
            break

        visited[u] = True

        for v, attr in G.adj[u].items():
            capacity = attr['capacity']
            flow = attr['flow']
            weight = attr['weight']
            if distance[u] + weight < distance[v] and flow < capacity:
                distance[v] = distance[u] + weight

    return distance

def mincost_maxflow(G: nx.DiGraph, source: int, sink: int) -> Tuple[int, int]:
    total_cost = 0
    total_flow = 0

    while True:
        distance = dijkstra(G, source)
        if distance[sink] == np.inf:
            break

        path = [sink]
        flow = np.inf

        while True:
            u = path[-1]
            if u == source:
                break

            for v, attr in G.succ[u].items():
                capacity = attr['capacity']
                f = min(capacity - attr['flow'], flow)
                if f > 0:
                    flow = f
                    path.append(v)
                    break

            if u == path[-1]:
                path.pop()

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            G.edges[u, v]['flow'] += flow
            G.edges[v, u]['flow'] -= flow

        cost = 0
        for u, v, attr in G.edges(data=True):
            cost += attr['flow'] * attr['weight']

        total_cost += cost
        total_flow += flow

    return total_cost, total_flow

# Przykładowe użycie
graph = nx.DiGraph()
graph.add_nodes_from(range(8))
u_edge = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 5]
v_edge = [1, 2, 3, 2, 3, 4, 3, 5, 6, 4, 5, 5, 7, 7, 5, 7, 6]
weights = [random.randint(1, 7) for _ in range(17)]
capacities = [random.randint(1, 7) for _ in range(17)]

for u, v, weight, capacity in zip(u_edge, v_edge, weights, capacities):
    graph.add_edge(u, v, weight=weight, capacity=capacity, flow=0)

source = 0
sink = 6

min_cost, max_flow = mincost_maxflow(graph, source, sink)
print("Minimalny koszt przepływu:", min_cost)
print("Maksymalny przepływ:", max_flow)
