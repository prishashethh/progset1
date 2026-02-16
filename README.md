# Partner A: Graph & Edge Manager (CS 1240 PA1)

## Your code

- **`graph_generator.py`** – Graph generation and edge pruning:
  - **Dimension 0:** Complete graph, edge weight = U[0,1]. Prune by threshold k(n).
  - **Dimension 1:** Hypercube: edge (a,b) iff |a−b| = 2^i. No pruning (O(n log n) edges).
  - **Dimensions 2, 3, 4:** Complete graph on random points in unit square/cube/4-cube; weight = Euclidean distance. Prune by k(n).
  - **Pruning:** `get_prune_threshold(n, dimension, grace=1.5)` gives k(n). Only edges with weight ≤ k(n) are kept so Kruskal only sorts O(n log n) edges instead of n².

- **`randmst.py`** – CLI and trial loop: parses `./randmst 0 numpoints numtrials dimension`, runs `numtrials` trials (each: generate pruned edges → MST), prints `average numpoints numtrials dimension`.

- **`mst.py`** – Wrapper that calls the MST algorithms and returns only the total weight. Uses **Prim's** for complete graphs (dimensions 0, 2, 3, 4) and **Kruskal's** for the hypercube (dimension 1).

- **`mst_algorithm.py`** – Partner B’s implementations of **Prim's** and **Kruskal's** MST. Takes an adjacency list, returns `(total_weight, list_of_edges)`. Do not modify this file.

### mst.py vs mst_algorithm.py

| | **mst_algorithm.py** | **mst.py** |
|---|------------------------|------------|
| **Role** | The actual MST algorithms (Prim, Kruskal). | Thin wrapper used by the rest of the project. |
| **Input** | Adjacency list `{v: [(neighbor, weight), ...]}`. | Same, plus `n` and `dimension`. |
| **Output** | `(total_weight, list_of_edges)`. | Just the total weight (float). |
| **Algorithm choice** | N/A — you call `prim(graph)` or `kruskal(graph)` directly. | Picks Prim for complete graphs (0,2,3,4), Kruskal for hypercube (1). |

**Note:** Importing `mst_algorithm` runs its example and prints two lines. `run_experiments.py` parses the **last** line of stdout so the real randmst output is still read correctly.

## Run

```bash
make randmst
./randmst 0 numpoints numtrials dimension
```
*(From the project directory.)*

Example: `./randmst 0 128 5 0` → average MST weight over 5 trials, n=128, dimension 0.

## Output for Partner B

`generate_pruned_edges(n, dimension, seed=..., grace=1.5)` returns an **adjacency list**: `{vertex: [(neighbor, weight), ...]}`. Partner B’s `prim` and `kruskal` in `mst_algorithm.py` consume this format.
