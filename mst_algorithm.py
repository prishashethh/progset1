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

class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def same_set(self, a, b):
        return self.find(a) == self.find(b)

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # union didn't happen

        # union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

        return True  # union happened

def kruskal(graph):
    vertices = getVertices(graph)
    if not vertices:
        return 0, []

    # Build undirected edge list with deduplication
    edges = []
    seen = set()
    for u in graph:
        for v, w in graph[u]:
            key = (u, v) if u <= v else (v, u)  # works if vertices are comparable
            if key in seen:
                continue
            seen.add(key)
            edges.append((u, v, w))

    edges.sort(key=lambda e: e[2])

    dsu = DisjointSet(vertices)
    mst_weight = 0
    mst_edges = []

    # Early stop once we have |V|-1 edges
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            mst_weight += w
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_weight, mst_edges
