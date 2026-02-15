def getVertices(graph):
    # Getting the vertices from the graph
    # Some vertices may be in the adjacency list, so we need to add them to the set
    vertices = set(graph.keys())
    for adj_list in graph.values():
        for (v, _) in adj_list:
            vertices.add(v)
    return vertices

# PRIM'S ALGORITHM 
# Min-heap (for Prim's)
def heapInsert(heap, key, val):
    heap.append((key, val))
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent][0] <= heap[i][0]:
            break
        heap[parent], heap[i] = heap[i], heap[parent]
        i = parent


def heapDeleteMin(heap):
    if not heap:
        raise IndexError("Empty heap")
    n = len(heap)
    out = heap[0]
    heap[0] = heap[n - 1]
    heap.pop()
    n -= 1
    i = 0
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < n and heap[left][0] < heap[smallest][0]:
            smallest = left
        if right < n and heap[right][0] < heap[smallest][0]:
            smallest = right
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
    return out

# Prim's algorithm 
def prim(graph, start=None):
    # Prim's algorithm for Minimum Spanning Tree
    vertices = getVertices(graph)

    # If there are no vertices, return 0 and an empty list
    if not vertices:
        return 0, []

    inf = float("inf")
    d = {v: inf for v in vertices}
    prev = {}
    S = set() # Set of vertices in the MST 

    if start is None:
        start = next(iter(vertices))
    if start not in vertices:
        raise ValueError(f"start vertex {start} not in graph")

    # Start vertex is picked first 
    d[start] = 0
    prev[start] = None
    heap = []
    heapInsert(heap, 0, start)

    # While the heap is not empty, we pick the minimum value from the heap
    while heap:
        key, u = heapDeleteMin(heap)
        if u in S:
            continue
        S.add(u)

        # For each vertex, we check if it is in the set of vertices in the MST 
        # and see what the weight of the edge is to the vertex to pick the min 
        for (v, w) in graph.get(u, []):
            if v not in S and w < d[v]:
                d[v] = w
                prev[v] = u
                heapInsert(heap, w, v)

    # Building the MST edge list and total weight
    finalWeight = 0
    finalEdges = []
    for v in S:
        if prev[v] is not None:
            w = d[v]
            finalWeight += w
            finalEdges.append((prev[v], v, w))

    return finalWeight, finalEdges

# KRUSKAL'S ALGORITHM 
# Disjoint Set Union-Find 
def makeSet(parent, rank, x):
    parent[x] = x
    rank[x] = 0

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  # path compression
    return parent[x]


def union(parent, rank, x, y):
    rx = find(parent, x)
    ry = find(parent, y)
    if rx == ry:
        return
    if rank[rx] < rank[ry]:
        parent[rx] = ry
    elif rank[ry] < rank[rx]:
        parent[ry] = rx
    else:
        parent[ry] = rx
        rank[rx] += 1


# The actual Kruskal's algorithm 
def kruskal(graph):
    # Getting the vertices from the graph
    vertices = getVertices(graph)
    if not vertices:
        return 0, []

    # Build list of all edges (u, v, w)
    edges = []
    for u in graph:
        for (v, w) in graph[u]:
            edges.append((u, v, w))

    edges.sort(key=lambda e: e[2])  # sort by weight

    parent = {}
    rank = {}
    for v in vertices:
        makeSet(parent, rank, v)

    # Building the MST edge list and total weight
    # We sort the edges by weight and then add the lightest edge that doesn't create a cycle
    finalWeight = 0
    finalEdges = []
    for (u, v, w) in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            finalWeight += w
            finalEdges.append((u, v, w))

    return finalWeight, finalEdges

# EXAMPLE 
graph10 = {
    "a": [("b", 4), ("c", 3), ("d", 7)],
    "b": [("a", 4), ("d", 6), ("e", 5)],
    "c": [("a", 3), ("d", 8), ("f", 10)],
    "d": [("a", 7), ("b", 6), ("c", 8), ("e", 2), ("g", 9)],
    "e": [("b", 5), ("d", 2), ("f", 1), ("h", 4)],
    "f": [("c", 10), ("e", 1), ("i", 3)],
    "g": [("d", 9), ("h", 2), ("j", 6)],
    "h": [("e", 4), ("g", 2), ("i", 5)],
    "i": [("f", 3), ("h", 5), ("j", 7)],
    "j": [("g", 6), ("i", 7)],
}

print(prim(graph10))
print(kruskal(graph10)) 