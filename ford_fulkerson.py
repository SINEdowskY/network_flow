import random
import networkx as nx

def ford_fulkerson(G, source, sink):
    for u, v in G.edges:
        G.edges[u, v]['flow'] = 0

    while True:
        path = bfs(G, source, sink)
        
        if not path:
            break
        
        min_capacity = float('inf')
        for u, v in zip(path, path[1:]):
            min_capacity = min(min_capacity, G.edges[u, v]['capacity'] - G.edges[u, v]['flow'])
        
        for u, v in zip(path, path[1:]):
            if G.has_edge(u, v):
                G.edges[u, v]['flow'] += min_capacity
            if G.has_edge(v, u):
                G.edges[v, u]['flow'] -= min_capacity
        
    total_flow = 0
    for u, v in G.edges:
        total_flow += G.edges[u, v]['flow']
    
    return total_flow

def bfs(G, source, sink):
    visited = {v: False for v in G.nodes}
    visited[source] = True
    
    path = {v: [] for v in G.nodes}
    queue = [source]
    
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            if not visited[v] and G.edges[u, v]['capacity'] > G.edges[u, v]['flow']:
                visited[v] = True
                path[v] = path[u] + [u]
                queue.append(v)
    
    if visited[sink]:
        path[sink] = path[sink] + [sink]
        return path[sink]
    else:
        return None