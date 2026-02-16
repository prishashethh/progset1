"""
Partner A: Graph & Edge Manager
Generates graph data for 5 scenarios (0D, 1D hypercube, 2D, 3D, 4D)
and prunes edges by threshold k(n) so we only pass the smallest edges for sorting.
"""

import json
import math
import random
import sys
import time
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


def generate_edges_0d(
    n: int, threshold: float, rng: random.Random, verbose: bool = False
) -> List[Tuple[int, int, float]]:
    """
    Dimension 0: Complete graph on n vertices, edge weight = U[0,1].
    Only keep edges with weight <= threshold (pruning).
    """
    edges: List[Tuple[int, int, float]] = []
    step = max(1, n // 10)
    for i in range(n):
        if verbose and i > 0 and (i % step == 0 or i == n - 1):
            print(f"    dim=0: vertex {i+1}/{n}", flush=True)
        for j in range(i + 1, n):
            w = rng.uniform(0, 1)
            if w <= threshold:
                edges.append((i, j, w))
    return edges


def generate_edges_1d_hypercube(
    n: int, rng: random.Random, verbose: bool = False
) -> List[Tuple[int, int, float]]:
    """
    Dimension 1: Hypercube. (a,b) is an edge iff |a-b| = 2^i for some i.
    Weight = U[0,1]. No pruning needed (only O(n log n) edges).
    """
    edges: List[Tuple[int, int, float]] = []
    gap = 1
    while gap < n:
        if verbose:
            print(f"    dim=1: gap={gap}, edges so far: {len(edges)}", flush=True)
        for a in range(n):
            b = a + gap
            if b < n:
                w = rng.uniform(0, 1)
                edges.append((a, b, w))
        gap *= 2
    return edges


def _euclidean(p: Tuple[float, ...], q: Tuple[float, ...]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def generate_edges_2d(
    n: int, threshold: float, rng: random.Random, verbose: bool = False
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit square; weight = Euclidean distance. Prune by threshold."""
    if verbose:
        print("    dim=2: generating points ...", flush=True)
    points: List[Tuple[float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n)
    ]
    if verbose:
        print("    dim=2: computing edges ...", flush=True)
    edges: List[Tuple[int, int, float]] = []
    step = max(1, n // 10)
    for i in range(n):
        if verbose and i > 0 and (i % step == 0 or i == n - 1):
            print(f"    dim=2: vertex {i+1}/{n}", flush=True)
        for j in range(i + 1, n):
            d = _euclidean(points[i], points[j])
            if d <= threshold:
                edges.append((i, j, d))
    return edges


def generate_edges_3d(
    n: int, threshold: float, rng: random.Random, verbose: bool = False
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit cube; weight = Euclidean distance. Prune by threshold."""
    if verbose:
        print("    dim=3: generating points ...", flush=True)
    points: List[Tuple[float, float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(n)
    ]
    if verbose:
        print("    dim=3: computing edges ...", flush=True)
    edges: List[Tuple[int, int, float]] = []
    step = max(1, n // 10)
    for i in range(n):
        if verbose and i > 0 and (i % step == 0 or i == n - 1):
            print(f"    dim=3: vertex {i+1}/{n}", flush=True)
        for j in range(i + 1, n):
            d = _euclidean(points[i], points[j])
            if d <= threshold:
                edges.append((i, j, d))
    return edges


def generate_edges_4d(
    n: int, threshold: float, rng: random.Random, verbose: bool = False
) -> List[Tuple[int, int, float]]:
    """Complete graph: n random points in unit 4-cube; weight = Euclidean distance. Prune by threshold."""
    if verbose:
        print("    dim=4: generating points ...", flush=True)
    points: List[Tuple[float, float, float, float]] = [
        (rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1))
        for _ in range(n)
    ]
    if verbose:
        print("    dim=4: computing edges ...", flush=True)
    edges: List[Tuple[int, int, float]] = []
    step = max(1, n // 10)
    for i in range(n):
        if verbose and i > 0 and (i % step == 0 or i == n - 1):
            print(f"    dim=4: vertex {i+1}/{n}", flush=True)
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


def write_graph_to_file(
    graph: Dict[int, List[Tuple[int, float]]],
    filepath: str,
    verbose: bool = False,
) -> None:
    """
    Write the adjacency list to a file for Partner B.
    Format: JSON with string keys (vertex -> list of [end_vertex, weight]).
    Partner B can load with: json.load(...) then convert keys back to int if needed.
    """
    if verbose:
        print(f"  Writing to {filepath} ...", flush=True)
    # JSON keys must be strings
    out = {str(v): [[u, w] for u, w in neighbors] for v, neighbors in graph.items()}
    with open(filepath, "w") as f:
        json.dump(out, f, indent=2)
    if verbose:
        print(f"  Done.", flush=True)


def generate_and_write(
    n: int,
    dimension: int,
    filepath: str,
    seed: Optional[int] = None,
    grace: float = 1.5,
    verbose: bool = False,
) -> Dict[int, List[Tuple[int, float]]]:
    """
    Generate pruned edges and write them to a file. Returns the graph as well.
    Example: generate_and_write(128, 0, "graph_n128_dim0.json", seed=0)
    """
    graph = generate_pruned_edges(n, dimension, seed=seed, grace=grace, verbose=verbose)
    write_graph_to_file(graph, filepath, verbose=verbose)
    return graph


def generate_pruned_edges(
    n: int,
    dimension: int,
    seed: Optional[int] = None,
    grace: float = 1.5,
    verbose: bool = False,
) -> Dict[int, List[Tuple[int, float]]]:
    """
    Generate edges for the given n and dimension, with pruning for complete graphs.
    Returns adjacency list: for each vertex, list of (end_vertex, weight) tuples.
    Example: {0: [(1, 0.5), (2, 0.3)], 1: [(0, 0.5), (3, 0.7)], ...}
    """
    if verbose:
        print(f"Generating graph: n={n}, dimension={dimension} ...", flush=True)
    t0 = time.time()
    rng = random.Random(seed)
    threshold = get_prune_threshold(n, dimension, grace=grace)
    if verbose and dimension != 1:
        print(f"  Prune threshold k(n) = {threshold:.6e}", flush=True)

    if dimension == 0:
        edges = generate_edges_0d(n, threshold, rng, verbose=verbose)
    elif dimension == 1:
        edges = generate_edges_1d_hypercube(n, rng, verbose=verbose)
    elif dimension == 2:
        edges = generate_edges_2d(n, threshold, rng, verbose=verbose)
    elif dimension == 3:
        edges = generate_edges_3d(n, threshold, rng, verbose=verbose)
    elif dimension == 4:
        edges = generate_edges_4d(n, threshold, rng, verbose=verbose)
    else:
        raise ValueError(f"Unsupported dimension: {dimension}")

    if verbose:
        print(f"  -> {len(edges)} edges in {time.time() - t0:.2f}s", flush=True)
        print("  Building adjacency list ...", flush=True)
    adj = _edge_list_to_adjacency(n, edges)
    if verbose:
        print(f"  Done. Total time: {time.time() - t0:.2f}s", flush=True)
    return adj


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 graph_generator.py <n> <dimension> [output.json]", file=sys.stderr)
        print("  n        = number of vertices", file=sys.stderr)
        print("  dimension = 0, 1, 2, 3, or 4", file=sys.stderr)
        print("  output.json = optional; if given, graph is written to this file.", file=sys.stderr)
        sys.exit(1)
    n = int(sys.argv[1])
    dimension = int(sys.argv[2])
    filepath = sys.argv[3] if len(sys.argv) > 3 else None
    if dimension not in (0, 1, 2, 3, 4):
        print("dimension must be 0, 1, 2, 3, or 4", file=sys.stderr)
        sys.exit(1)
    if filepath:
        generate_and_write(n, dimension, filepath, seed=0, verbose=True)
        print(f"Graph written to {filepath}", flush=True)
    else:
        generate_pruned_edges(n, dimension, seed=0, verbose=True)
