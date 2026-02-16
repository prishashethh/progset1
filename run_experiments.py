#!/usr/bin/env python3
"""
Run all experiments for the PA1 report.
Outputs tables of average MST weight for each graph type and n value.
"""

import subprocess
import sys

NUM_TRIALS = 5

COMPLETE_GRAPH_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
HYPERCUBE_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]

DIMENSION_NAMES = {
    0: "0D Complete (U[0,1] weights)",
    1: "1D Hypercube",
    2: "2D (unit square)",
    3: "3D (unit cube)",
    4: "4D (unit hypercube)",
}


def run_single(n: int, dim: int) -> float:
    """Run randmst and return average MST weight."""
    result = subprocess.run(
        [sys.executable, "randmst.py", "0", str(n), str(NUM_TRIALS), str(dim)],
        capture_output=True,
        text=True,
        cwd=".",
    )
    result.check_returncode()
    # Last line is randmst output (mst_algorithm may print example when imported)
    lines = result.stdout.strip().split("\n")
    avg = float(lines[-1].split()[0])
    return avg


def main() -> None:
    # Complete graphs: dimensions 0, 2, 3, 4
    for dim in [0, 2, 3, 4]:
        print(f"\n{'='*60}")
        print(f"Dimension {dim}: {DIMENSION_NAMES[dim]}")
        print("=" * 60)
        print(f"{'n':>10} | {'Avg MST Weight':>16}")
        print("-" * 30)
        for n in COMPLETE_GRAPH_NS:
            try:
                avg = run_single(n, dim)
                print(f"{n:>10} | {avg:>16.6f}")
            except Exception as e:
                print(f"{n:>10} | ERROR: {e}")

    # Hypercube: dimension 1
    dim = 1
    print(f"\n{'='*60}")
    print(f"Dimension {dim}: {DIMENSION_NAMES[dim]}")
    print("=" * 60)
    print(f"{'n':>10} | {'Avg MST Weight':>16}")
    print("-" * 30)
    for n in HYPERCUBE_NS:
        try:
            avg = run_single(n, dim)
            print(f"{n:>10} | {avg:>16.6f}")
        except Exception as e:
            print(f"{n:>10} | ERROR: {e}")

    print("\nDone. Copy the tables above into your report.")


if __name__ == "__main__":
    main()
