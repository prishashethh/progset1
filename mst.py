# MST weight using the mst_algorithm
from typing import Dict, List, Tuple

from mst_algorithm import kruskal, prim


def mst_weight(
    n: int,
    graph: Dict[int, List[Tuple[int, float]]],
    dimension: int,
) -> float:

    # We use Prim's for complete graphs (0,2,3,4), and Kruskals for the hypercube (1)
    if dimension == 1:
        weight, _ = kruskal(graph)
    else:
        weight, _ = prim(graph)
    return weight
