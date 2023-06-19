import networkx as nx

def bellman_ford_shortest_augmenting_path(graph, source, sink):
    # 1. Inicjalizuj odległości wszystkich wierzchołków jako nieskończoność,
    # z wyjątkiem wierzchołka źródłowego, którego odległość ustaw na 0.
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    predecessors = {}

    # 2. Wykonaj relaksację krawędzi dla każdej krawędzi grafu.
    # Relaksacja oznacza sprawdzenie, czy możliwe jest skrócenie aktualnej odległości do danego wierzchołka
    # poprzez skorzystanie z danej krawędzi.
    # Jeśli tak, zaktualizuj odległość wierzchołka na wartość mniejszą.
    # Powtarzaj krok 2 dla wszystkich krawędzi grafu V-1 razy, 
    # gdzie V to liczba wierzchołków.
    # To pozwala na rozważenie najdłuższych ścieżek w grafie.

    for _ in range(len(graph.nodes) - 1):
        for u, v, attr in graph.edges(data=True):
            weight = attr['weight']
            capacity = attr['capacity']
            flow = attr['flow']
            if flow < capacity and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u

    # Sprawdzenie czy istnieje ścieżka powiększająca
    if sink not in predecessors:
        return None

    # Odtworzenie ścieżki powiększającej
    path = [sink]
    while path[-1] != source:
        path.append(predecessors[path[-1]])
    path.reverse()

    return path

def min_cost_max_flow(graph, source, sink):
    flow_value = 0
    cost_value = 0
    path = bellman_ford_shortest_augmenting_path(graph, source, sink)

    while path is not None:
        # Wyszukiwanie maksymalnego przepływu na ścieżce powiększającej
        min_capacity = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity = graph[u][v]['capacity']
            flow = graph[u][v]['flow']
            min_capacity = min(min_capacity, capacity - flow)

        # Aktualizacja przepływu i kosztu
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if graph.has_edge(u, v):
                graph[u][v]['flow'] += min_capacity
                graph[u][v]['cost'] = -graph[u][v]['weight']
            if graph.has_edge(v, u):
                graph[v][u]['flow'] -= min_capacity
                graph[v][u]['cost'] = graph[v][u]['weight']
            cost_value += min_capacity * graph[u][v]['weight']

        flow_value += min_capacity

        # Wyszukiwanie kolejnej ścieżki powiększającej
        path = bellman_ford_shortest_augmenting_path(graph, source, sink)

    return flow_value, cost_value
