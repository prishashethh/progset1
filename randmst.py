#!/usr/bin/env python3
"""
randmst: Command-line interface and trial loop.
Usage: ./randmst 0 numpoints numtrials dimension
Output: average numpoints numtrials dimension
"""

import sys

from graph_generator import generate_pruned_edges
from mst import mst_weight


def run_trial(n: int, dimension: int, trial_index: int) -> float:
    """One trial: generate graph, compute MST weight using mst_algorithm."""
    graph = generate_pruned_edges(n, dimension, seed=trial_index, grace=1.5)
    return mst_weight(n, graph, dimension)


def main() -> None:
    if len(sys.argv) != 5:
        print("Usage: randmst 0 numpoints numtrials dimension", file=sys.stderr)
        sys.exit(1)
    _flag = sys.argv[1]
    numpoints = int(sys.argv[2])
    numtrials = int(sys.argv[3])
    dimension = int(sys.argv[4])

    if numpoints < 2:
        print("numpoints must be >= 2", file=sys.stderr)
        sys.exit(1)
    if numtrials < 1:
        print("numtrials must be >= 1", file=sys.stderr)
        sys.exit(1)
    if dimension not in (0, 1, 2, 3, 4):
        print("dimension must be 0, 1, 2, 3, or 4", file=sys.stderr)
        sys.exit(1)

    total_weight = 0.0
    for t in range(numtrials):
        total_weight += run_trial(numpoints, dimension, t)

    average = total_weight / numtrials
    print(f"{average} {numpoints} {numtrials} {dimension}")


if __name__ == "__main__":
    main()
