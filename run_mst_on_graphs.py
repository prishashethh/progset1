#!/usr/bin/env python3
"""
Partner B: Load graphs from generated_graphs/, run MST (Prim or Kruskal), report weights.

Usage:
  python3 run_mst_on_graphs.py [generated_graphs]
  python3 run_mst_on_graphs.py --out results.txt

If no directory is given, uses ./generated_graphs.
"""

import json
import os
import re
import sys
from typing import Dict, List, Tuple

from mst_algorithm import kruskal, prim

GRAPH_DIR = "generated_graphs"
# Filename pattern: graph_n128_dim0.json -> n=128, dim=0
PATTERN = re.compile(r"graph_n(\d+)_dim(\d+)\.json")


def load_graph(filepath: str) -> Tuple[Dict[int, List[Tuple[int, float]]], int, int]:
    """
    Load a graph JSON from Partner A. Returns (graph, n, dimension).
    graph format: {vertex: [(neighbor, weight), ...]} with int keys.
    """
    with open(filepath) as f:
        raw = json.load(f)
    graph: Dict[int, List[Tuple[int, float]]] = {}
    for v_str, neighbors in raw.items():
        v = int(v_str)
        graph[v] = [(int(u), float(w)) for u, w in neighbors]
    # n = number of vertices (max key + 1 or len(vertices))
    vertices = set(graph.keys())
    for adj in graph.values():
        for u, _ in adj:
            vertices.add(u)
    n = max(vertices) + 1 if vertices else 0
    return graph, n, -1  # dimension not in file; caller gets it from filename


def dimension_from_filename(filename: str) -> int:
    """Parse dimension from graph_n<N>_dim<D>.json -> D."""
    m = PATTERN.search(filename)
    return int(m.group(2)) if m else -1


def mst_weight_for_graph(graph: Dict[int, List[Tuple[int, float]]], dimension: int) -> float:
    """Use Prim for complete graphs (0,2,3,4), Kruskal for hypercube (1)."""
    if dimension == 1:
        weight, _ = kruskal(graph)
    else:
        weight, _ = prim(graph)
    return weight


def main() -> None:
    out_file = None
    graph_dir = GRAPH_DIR
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_file = args[i + 1]
            i += 2
        elif not args[i].startswith("-"):
            graph_dir = args[i]
            i += 1
        else:
            i += 1

    if not os.path.isdir(graph_dir):
        print(f"Directory not found: {graph_dir}", file=sys.stderr)
        print("Usage: python3 run_mst_on_graphs.py [generated_graphs] [--out results.txt]", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(graph_dir) if f.endswith(".json") and PATTERN.search(f))
    if not files:
        print(f"No graph_n*_dim*.json files in {graph_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Partner B: running MST on {len(files)} graphs in {graph_dir}/")
    print("=" * 60)

    lines: List[str] = []
    for f in files:
        filepath = os.path.join(graph_dir, f)
        dim = dimension_from_filename(f)
        try:
            graph, n, _ = load_graph(filepath)
            weight = mst_weight_for_graph(graph, dim)
            line = f"{f}: n={n} dim={dim}  MST weight = {weight:.6f}"
            print(line)
            lines.append(line)
        except Exception as e:
            line = f"{f}: ERROR {e}"
            print(line)
            lines.append(line)

    print("=" * 60)
    print("Done.")

    if out_file:
        with open(out_file, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Results written to {out_file}")


if __name__ == "__main__":
    main()
