"""
MST weight computation using mst_algorithm (Prim's and Kruskal's).
- Use Prim's for complete graphs (dimensions 0, 2, 3, 4).
- Use Kruskal's for hypercube (dimension 1).
"""

from typing import Dict, List, Tuple

from mst_algorithm import kruskal, prim


def mst_weight(
    n: int,
    graph: Dict[int, List[Tuple[int, float]]],
    dimension: int,
) -> float:
    """
    Compute MST total weight for the given adjacency list graph.
    graph: {vertex: [(neighbor, weight), ...]}
    dimension: 0,1,2,3,4 - used to select Prim's (complete) vs Kruskal's (hypercube).
    """
    if dimension == 1:
        weight, _ = kruskal(graph)
    else:
        weight, _ = prim(graph)
    return weight
