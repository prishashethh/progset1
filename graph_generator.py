import math
import random

# Euclidean distance between two points as we need
def euclidean(p, q):
    s = 0.0
    for a, b in zip(p, q):
        d = a - b
        s += d * d
    return math.sqrt(s)

def get_prune_threshold(n, dimension, grace=2.0):
    # listening to the hint, only keep edges with weight <= k(n) that we found empiracally
    if n <= 1:
        return float("inf")
    ln_n = math.log(n)

    if dimension == 0:
        return (ln_n / n) * grace
    if dimension == 1:
        return float("inf")  # already sparse
    if dimension == 2:
        return math.sqrt(ln_n / n) * grace
    if dimension == 3:
        return (ln_n / n) ** (1/3) * grace
    if dimension == 4:
        return (ln_n / n) ** (1/4) * grace
    return float("inf")

def neighbor_buckets(index):
    d = len(index)
    shifts = [[]]
    for _ in range(d):
        new_shifts = []
        for sh in shifts:
            for step in (-1, 0, 1):
                new_shifts.append(sh + [step])
        shifts = new_shifts

    out = []
    for sh in shifts:
        out.append(tuple(index[i] + sh[i] for i in range(d)))
    return out

def edge_list_to_adjacency(vertices, edges):
    graph = {v: [] for v in vertices}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph


def generate_graph(n, dimension, seed=None, grace=2.0):
    # 0: complete graph on vertices 0..n-1, weights U[0,1], pruned by k(n)
    # 1: "hypercube" edges |a-b| = 2^i, weights U[0,1]
    # 2/3/4: points in unit cube of that dimension, Euclidean weights

    rng = random.Random(seed)

    # dimension 0 (random edge weights on complete graph) 
    if dimension == 0:
        vertices = list(range(n))
        thr = get_prune_threshold(n, 0, grace=grace)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                w = rng.random()
                if w <= thr:
                    edges.append((i, j, w))
        return edge_list_to_adjacency(vertices, edges)

    # dimension 1 ("hypercube")
    if dimension == 1:
        vertices = list(range(n))
        edges = []
        gap = 1
        while gap < n:
            for a in range(n):
                b = a + gap
                if b < n:
                    edges.append((a, b, rng.random()))
            gap *= 2
        return edge_list_to_adjacency(vertices, edges)

    # dimensions 2/3/4 (geometric complete graph, but optimized)
    if dimension not in (2, 3, 4):
        raise ValueError("dimension must be 0, 1, 2, 3, or 4")

    d = dimension

    # Generate unique points stored in the set
    vertices = []
    seen = set()
    while len(vertices) < n:
        p = tuple(round(rng.random(), 5) for _ in range(d))
        if p not in seen:
            seen.add(p)
            vertices.append(p)

    # Avoid O(n^2) by bucketing 
    bucket_side = (4.0 / n) ** (1.0 / d)

    buckets = {}
    for v in vertices:
        idx = tuple(int(coord // bucket_side) for coord in v)
        buckets.setdefault(idx, []).append(v)

    bucket_keys = sorted(buckets.keys())

    # Threshold prune to keep the number of edges O(n log n)
    thr = get_prune_threshold(n, d, grace=grace)

    edges = []
    for bk in bucket_keys:
        for nb in neighbor_buckets(bk):

            # skip nonexistent buckets + avoid double counting
            if nb not in buckets or nb < bk:
                continue

            if nb == bk:
                pts = buckets[bk]
                for i in range(len(pts)):
                    for j in range(i + 1, len(pts)):
                        w = euclidean(pts[i], pts[j])
                        if w <= thr:
                            edges.append((pts[i], pts[j], w))
            else:
                for p in buckets[bk]:
                    for q in buckets[nb]:
                        w = euclidean(p, q)
                        if w <= thr:
                            edges.append((p, q, w))

    return edge_list_to_adjacency(vertices, edges)


def generate_pruned_edges(n, dimension, seed=None, grace=2.0, verbose=False):
    if verbose:
        print(f"[graph_generator] n={n} dim={dimension} seed={seed} grace={grace}", flush=True)
    return generate_graph(n, dimension, seed=seed, grace=grace)


import json

def generate_and_write(n, dimension, filepath, seed=None, grace=2.0, verbose=False):
    # Generate a graph and write it to a file
    if verbose:
        print(f"  Generating graph (n={n}, dim={dimension}, seed={seed}, grace={grace}) ...", flush=True)

    graph = generate_graph(n, dimension, seed=seed, grace=grace)

    if verbose:
        # quick summary
        m = sum(len(adj) for adj in graph.values()) // 2
        print(f"  Built adjacency list: |V|={len(graph)}, |E|≈{m}", flush=True)
        print(f"  Writing to {filepath} ...", flush=True)

    # JSON requires string keys; neighbors written as [neighbor, weight]
    out = {str(v): [[u, w] for (u, w) in neighbors]
           for v, neighbors in graph.items()}

    with open(filepath, "w") as f:
        json.dump(out, f, indent=2)

    if verbose:
        print("  Done.", flush=True)

    return graph
