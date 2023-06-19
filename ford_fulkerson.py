import random
import networkx as nx

def ford_fulkerson(G: nx.DiGraph, source, sink):
    # 1. Inicjalizuj przepływ na wszystkich krawędziach w sieci na wartość 0.
    for u, v in G.edges:
        G.edges[u, v]['flow'] = 0

    # 2. Dopóki istnieje ścieżka powiększająca w sieci rezydualnej 
    # (czyli w sieci, gdzie przepływ odejmujemy od pojemności krawędzi),
    # wykonuj następujące kroki:
    while True:
        # a. Wyszukaj ścieżkę powiększającą, za pomocą przeszukiwania wszerz (BFS). 
        # Ścieżka powiększająca to ścieżka od źródła do ujścia, 
        # w której żadna krawędź nie ma maksymalnego przepływu.
        path = bfs(G, source, sink)
        
        if not path:
            break
        # b. Znajdź minimalną wartość przepustowości na ścieżce powiększającej,
        # określmy ją jako `min_capacity`.
        min_capacity = float('inf')
        for u, v in zip(path, path[1:]):
            min_capacity = min(min_capacity, G.edges[u, v]['capacity'] - G.edges[u, v]['flow'])
        
        for u, v in zip(path, path[1:]):
            # c. Zwiększ przepływ na każdej krawędzi w ścieżce powiększającej o wartość `min_capacity`.
            if G.has_edge(u, v):
                G.edges[u, v]['flow'] += min_capacity
            # d. Zmniejsz przepływ na każdej krawędzi w ścieżce powrotnej o wartość `min_capacity`.
            if G.has_edge(v, u):
                G.edges[v, u]['flow'] -= min_capacity
        #3. Oblicz wartość przepływu jako suma przepływów wychodzących z źródła
        max_flow = 0
        sink_neighbors = [n for n in G.neighbors(source)]
        for neighbor in sink_neighbors:
            max_flow += G[source][neighbor]['flow']

    return max_flow

def bfs(G, source, sink):
    # 1. Wybierz wierzchołek startowy, oznacz go jako odwiedzony i umieść go w kolejce.
    visited = {v: False for v in G.nodes}
    visited[source] = True
    
    path = {v: [] for v in G.nodes}
    queue = [source]
    # 2. Dopóki kolejka nie jest pusta, wykonuj następujące kroki: 
    while queue:
        # a. Pobierz wierzchołek z przodu kolejki. 
        u = queue.pop(0)
        # b. Przejdź przez wszystkich nieodwiedzonych sąsiadów danego wierzchołka.
        for v in G.neighbors(u):
            if not visited[v] and G.edges[u, v]['capacity'] > G.edges[u, v]['flow']:
                # c. Oznacz każdego sąsiada jako odwiedzonego,
                # umieść go w kolejce i ustaw jego poprzednika na bieżący wierzchołek.
                visited[v] = True
                path[v] = path[u] + [u]
                queue.append(v)
    
    if visited[sink]:
        path[sink] = path[sink] + [sink]
        return path[sink]
    else:
        return None