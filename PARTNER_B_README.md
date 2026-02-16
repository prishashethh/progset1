# Partner B: Using the graphs in `generated_graphs/`

Partner A has written one JSON file per graph to **`generated_graphs/`** (or the directory you used with `generate_all_graphs.py --out DIR`). Each file is named like `graph_n128_dim0.json` (n = number of vertices, dim = dimension 0–4).

## What to do

### 1. Run MST on all graphs and see results in the terminal

From the project root (where `mst_algorithm.py` and `run_mst_on_graphs.py` live):

```bash
python3 run_mst_on_graphs.py
```

This uses **`generated_graphs/`** by default. It will:

- Load every `graph_n*_dim*.json` in that folder
- For each file: convert JSON → adjacency list (int keys, `(neighbor, weight)` tuples)
- Choose **Prim’s** for dim 0, 2, 3, 4 and **Kruskal’s** for dim 1 (hypercube)
- Print one line per graph: filename, n, dim, MST weight

### 2. Run MST on a different directory

```bash
python3 run_mst_on_graphs.py /path/to/my/graphs
```

### 3. Save the results to a file

```bash
python3 run_mst_on_graphs.py --out results.txt
python3 run_mst_on_graphs.py /path/to/graphs --out results.txt
```

---

## Graph format (what Partner A gives you)

Each JSON file is an adjacency list:

- **Keys:** vertex ids (strings in JSON, e.g. `"0"`, `"1"`).
- **Values:** list of `[end_vertex, weight]` (two numbers per edge).

Example:

```json
{
  "0": [[1, 0.5], [2, 0.3]],
  "1": [[0, 0.5], [3, 0.7]],
  "2": [[0, 0.3]],
  "3": [[1, 0.7]]
}
```

`run_mst_on_graphs.py` converts this to the format `mst_algorithm` expects: **int** keys and lists of **(neighbor, weight)** tuples.

---

## Algorithm choice

- **Dimension 0, 2, 3, 4** (complete graphs): use **Prim’s** (`mst_algorithm.prim`).
- **Dimension 1** (hypercube): use **Kruskal’s** (`mst_algorithm.kruskal`).

The script picks the algorithm from the filename (`dim0` … `dim4`).

---

## If you want to load one file in your own code

```python
import json
from mst_algorithm import prim, kruskal

with open("generated_graphs/graph_n128_dim0.json") as f:
    raw = json.load(f)

# Convert to format mst_algorithm expects: int keys, (neighbor, weight) tuples
graph = {int(v): [(int(u), float(w)) for u, w in neighbors] for v, neighbors in raw.items()}

# Use Prim for complete graphs (dim 0,2,3,4), Kruskal for dim 1
weight, edges = prim(graph)   # or kruskal(graph) for hypercube
print("MST weight:", weight)
```

---

**Note:** When you run the script, the first two lines of output may be from `mst_algorithm`’s built-in example (running `prim` and `kruskal` on a small test graph). The rest is the per-file MST output from `run_mst_on_graphs.py`.
