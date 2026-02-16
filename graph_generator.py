"""
Partner A: Graph & Edge Manager
Generates graph data for 5 scenarios (0D, 1D hypercube, 2D, 3D, 4D)
and prunes edges by threshold k(n) so we only pass the smallest edges for sorting.
"""

import math
import random
from typing import Dict, List, Optional, Tuple


def get_prune_threshold(n: int, dimension: int, grace: float = 1.5) -> float:
    """
    Threshold k(n) for edge pruning. Only edges with weight <= k(n) are kept.
    Based on known MST max-edge growth; we add grace so we never discard an MST edge.
    Throwing away edges above k(n) never gives wrong tree because the MST only uses
    the smallest n-1 edges that connect the graph, and they are all below this bound w.h.p.
    """
    if n <= 1:
        return float("inf")
    ln_n = math.log(n)
    if dimension == 0:
        # Complete graph U[0,1]: max MST edge ~ (1+o(1)) * ln(n)/n
        k = (ln_n / n) * grace
    elif dimension == 1:
        # Hypercube: no pruning (few edges); return infinity
        return float("inf")
    elif dimension == 2:
        # Unit square: max MST edge ~ O(sqrt(ln n / n))
        k = math.sqrt(ln_n / n) * grace
    elif dimension == 3:
        k = (ln_n / n) ** (1 / 3) * grace
    elif dimension == 4:
        k = (ln_n / n) ** (1 / 4) * grace
    else:
        k = float("inf")
    return max(k, 1e-10)  # avoid zero


def generate_edges_0d(n: int, threshold: float, rng: random.Random) -> List[Tuple[int, int, float]]:
    """
    Dimension 0: Complete graph on n vertices, edge weight = U[0,1].
    Only keep edges with weight <= threshold (pruning).
    """
    edges: List[Tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            w = rng.uniform(0, 1)
            if w <= threshold:
                edges.append((i, j, w))
    return edges


def generate_edges_1d_hypercube(n: int, rng: random.Random) -> List[Tuple[int, int, float]]:
    """
    Dimension 1: Hypercube. (a,b) is an edge iff |a-b| = 2^i for some i.
    Weight = U[0,1]. No pruning needed (only O(n log n) edges).
    """
    edges: List[Tuple[int, int, float]] = []
    i = 1
    while i < n:
        for a in range(n):
            b = a + i
            if b < n:
                w = rng.uniform(0, 1)
                edges.append((a, b, w))
        i *= 2
    return edges


def _euclidean(p: Tuple[float, ...], q: Tuple[float, ...]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def generate_edges_2d(
    n: int, threshold: float, rng: random.Random
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit square; weight = Euclidean distance. Prune by threshold."""
    points: List[Tuple[float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n)
    ]
    edges: List[Tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            d = _euclidean(points[i], points[j])
            if d <= threshold:
                edges.append((i, j, d))
    return edges


def generate_edges_3d(
    n: int, threshold: float, rng: random.Random
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit cube; weight = Euclidean distance. Prune by threshold."""
    points: List[Tuple[float, float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n)
    ]
    edges: List[Tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            d = _euclidean(points[i], points[j])
            if d <= threshold:
                edges.append((i, j, d))
    return edges


def generate_edges_4d(
    n: int, threshold: float, rng: random.Random
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit 4-cube; weight = Euclidean distance. Prune by threshold."""
    points: List[Tuple[float, float, float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1))
        for _ in range(n)
    ]
    edges: List[Tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            d = _euclidean(points[i], points[j])
            if d <= threshold:
                edges.append((i, j, d))
    return edges


def _edge_list_to_adjacency(n: int, edges: List[Tuple[int, int, float]]) -> Dict[int, List[Tuple[int, float]]]:
    """
    Convert flat edge list [(u, v, w), ...] to adjacency list:
    {vertex: [(neighbor, weight), ...]} for each vertex.
    """
    adj: Dict[int, List[Tuple[int, float]]] = {v: [] for v in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def generate_pruned_edges(
    n: int,
    dimension: int,
    seed: Optional[int] = None,
    grace: float = 1.5,
) -> Dict[int, List[Tuple[int, float]]]:
    """
    Generate edges for the given n and dimension, with pruning for complete graphs.
    Returns adjacency list: for each vertex, list of (end_vertex, weight) tuples.
    Example: {0: [(1, 0.5), (2, 0.3)], 1: [(0, 0.5), (3, 0.7)], ...}
    """
    rng = random.Random(seed)
    threshold = get_prune_threshold(n, dimension, grace=grace)

    if dimension == 0:
        edges = generate_edges_0d(n, threshold, rng)
    elif dimension == 1:
        edges = generate_edges_1d_hypercube(n, rng)
    elif dimension == 2:
        edges = generate_edges_2d(n, threshold, rng)
    elif dimension == 3:
        edges = generate_edges_3d(n, threshold, rng)
    elif dimension == 4:
        edges = generate_edges_4d(n, threshold, rng)
    else:
        raise ValueError(f"Unsupported dimension: {dimension}")

    return _edge_list_to_adjacency(n, edges)
