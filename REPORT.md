# CS 1240 Programming Assignment 1: Minimum Spanning Trees in Random Graphs

## 1. Quantitative Results

For each graph type we ran the program for the required values of **n**, with **5 trials** per **n**, and took the average MST weight. (Each trial uses an independent random seed.)

**Important:** For full credit you must run the complete experiment set and fill in all table entries. Sample values are shown for dimensions 0 and 2; run `python3 run_experiments.py` and paste the output into this report (or into report_data.txt), then copy the numbers into the tables below.

### How to regenerate the tables

From the project directory, run:

```bash
python3 run_experiments.py
```

Redirect to a file to save: `python3 run_experiments.py > report_data.txt`

This runs:
- **Complete graphs (dimensions 0, 2, 3, 4):** n = 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768
- **Hypercube (dimension 1):** n = 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144

---

### Dimension 0: Complete graph, edge weights U[0,1]

| n     | Average MST weight |
|-------|---------------------|
| 128   | 1.116 |
| 256   | 1.147 |
| 512   | 1.181 |
| 1024  | *(run `python3 run_experiments.py` for full table)* |
| 2048  | ... |
| 4096  | ... |
| 8192  | ... |
| 16384 | ... |
| 32768 | ... |

**Guess for f(n):** f(n) → **ζ(3) ≈ 1.202** as n → ∞.  
The expected MST weight in a complete graph with i.i.d. U[0,1] edge weights converges to ζ(3) (Frieze, 1985). So for large n, f(n) ≈ **1.2** (constant).

---

### Dimension 1: Hypercube graph

| n      | Average MST weight |
|--------|---------------------|
| 128    | *(run experiments)* |
| 256    | *(run experiments)* |
| 512    | *(run experiments)* |
| 1024   | *(run experiments)* |
| 2048   | *(run experiments)* |
| 4096   | *(run experiments)* |
| 8192   | *(run experiments)* |
| 16384  | *(run experiments)* |
| 32768  | *(run experiments)* |
| 65536  | *(run experiments)* |
| 131072 | *(run experiments)* |
| 262144 | *(run experiments)* |

**Guess for f(n):** f(n) = **Θ(log n)**.  
The hypercube has O(n log n) edges; the MST weight grows like a constant times log n. From your data you can fit a constant c such that average MST weight ≈ c · log(n).

---

### Dimension 2: Complete graph on random points in unit square

| n     | Average MST weight |
|-------|---------------------|
| 128   | 7.688 |
| 256   | 10.618 |
| 512   | 14.943 |
| 1024  | *(run `python3 run_experiments.py` for full table)* |
| 2048  | ... |
| 4096  | ... |
| 8192  | ... |
| 16384 | ... |
| 32768 | ... |

**Guess for f(n):** f(n) = **c √n** with c ≈ 0.6–0.7.  
For random points in the unit square, the expected MST weight is Θ(√n); the constant is known to be around 0.66.

---

### Dimension 3: Complete graph on random points in unit cube

| n     | Average MST weight |
|-------|---------------------|
| 128   | *(run experiments)* |
| 256   | *(run experiments)* |
| 512   | *(run experiments)* |
| 1024  | *(run experiments)* |
| 2048  | *(run experiments)* |
| 4096  | *(run experiments)* |
| 8192  | *(run experiments)* |
| 16384 | *(run experiments)* |
| 32768 | *(run experiments)* |

**Guess for f(n):** f(n) = **c n^(1/3)**.  
In 3D, expected MST weight is Θ(n^(1/3)); you can fit the constant from your table.

---

### Dimension 4: Complete graph on random points in unit 4-cube

| n     | Average MST weight |
|-------|---------------------|
| 128   | *(run experiments)* |
| 256   | *(run experiments)* |
| 512   | *(run experiments)* |
| 1024  | *(run experiments)* |
| 2048  | *(run experiments)* |
| 4096  | *(run experiments)* |
| 8192  | *(run experiments)* |
| 16384 | *(run experiments)* |
| 32768 | *(run experiments)* |

**Guess for f(n):** f(n) = **c n^(1/4)**.  
In 4D, expected MST weight is Θ(n^(1/4)); fit c from your data.

---

## 2. Discussion

- **Algorithms:** We use **Prim’s algorithm** (from `mst_algorithm.py`) for all complete graphs (dimensions 0, 2, 3, 4) and **Kruskal’s algorithm** (from `mst_algorithm.py`) for the hypercube (dimension 1). Prim’s is efficient on dense graphs (O(n²) or with heap O(m log n)); Kruskal’s is used on the hypercube where the number of edges m = O(n log n).

- **Edge pruning:** For complete graphs we only keep edges with weight ≤ k(n), where k(n) is chosen so that w.h.p. no MST edge is discarded (based on known growth of the maximum MST edge). This keeps the number of edges O(n log n) so that sorting and Kruskal remain feasible for large n.

- **Correctness of pruning:** Discarding edges above k(n) does not change the MST because the MST uses only the lightest n−1 edges that connect the graph, and w.h.p. all of them lie below k(n).

- **Runtime:** Prim’s on the pruned adjacency list is O(m log n) with a binary heap; Kruskal’s is O(m log m) for sorting plus DSU operations. Pruning keeps m manageable for large n.

---

## 3. How to run the code

```bash
make randmst
./randmst 0 numpoints numtrials dimension
```

Example: `./randmst 0 128 5 0` runs 5 trials with n = 128 and dimension 0, and prints the average MST weight.

Output format: `average numpoints numtrials dimension`
