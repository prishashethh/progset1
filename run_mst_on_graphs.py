import json
import os
import re
import sys
from typing import Dict, List, Tuple

from mst_algorithm import kruskal, prim

GRAPH_DIR = "generated_graphs"
PATTERN = re.compile(r"graph_n(\d+)_dim(\d+)\.json")

# Takes our generated graph and runs them 
# For our experiements, we have JSON files that open filepaths 
# and then turns them into our dictionary of int keys and lists of tuples
def loadGraph(filepath: str) -> Tuple[Dict[int, List[Tuple[int, float]]], int, int]:
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
    return graph, n, -1 


def dimensionFilename(filename: str) -> int:
    m = PATTERN.search(filename)
    return int(m.group(2)) if m else -1


def mstWeight(graph: Dict[int, List[Tuple[int, float]]], dimension: int) -> float:
    # Lowkey got a hint from Shlok's office hours, but it makes sense
    # We use Prim's for complete graphs (0,2,3,4), and Kruskals for the hypercube (1)
    if dimension == 1:
        weight, _ = kruskal(graph)
    else:
        weight, _ = prim(graph)
    return weight


def main() -> None:
    out_file = None
    graphDir = GRAPH_DIR
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_file = args[i + 1]
            i += 2
        elif not args[i].startswith("-"):
            graphDir = args[i]
            i += 1
        else:
            i += 1

    if not os.path.isdir(graphDir):
        print(f"Directory not found: {graphDir}", file=sys.stderr)
        print("Usage: python3 run_mst_on_graphs.py [generated_graphs] [--out results.txt]", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(graphDir) if f.endswith(".json") and PATTERN.search(f))
    if not files:
        print(f"No graph_n*_dim*.json files in {graphDir}", file=sys.stderr)
        sys.exit(1)

    lines: List[str] = []
    for f in files:
        filepath = os.path.join(graphDir, f)
        dim = dimensionFilename(f)
        try:
            graph, n, _ = loadGraph(filepath)
            weight = mstWeight(graph, dim)
            line = f"{f}: n={n} dim={dim}  MST weight = {weight:.6f}"
            print(line)
            lines.append(line)
        except Exception as e:
            line = f"{f}: ERROR {e}"
            print(line)
            lines.append(line)

    if out_file:
        with open(out_file, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Results written to {out_file}")

if __name__ == "__main__":
    main()
