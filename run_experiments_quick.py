#!/usr/bin/env python3
"""Quick experiment run (subset of n) for testing and report draft."""

import subprocess
import sys

NUM_TRIALS = 5
COMPLETE_NS = [128, 256, 512, 1024, 2048, 4096, 8192]
HYPERCUBE_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384]

def run_single(n: int, dim: int) -> float:
    result = subprocess.run(
        [sys.executable, "randmst.py", "0", str(n), str(NUM_TRIALS), str(dim)],
        capture_output=True, text=True, cwd=".",
    )
    result.check_returncode()
    return float(result.stdout.strip().split("\n")[-1].split()[0])

def main():
    for dim in [0, 2, 3, 4]:
        print(f"\nDim {dim}: ", end="")
        for n in COMPLETE_NS:
            print(f" {run_single(n, dim):.4f}", end="")
        print()
    print("\nDim 1 (hypercube): ", end="")
    for n in HYPERCUBE_NS:
        print(f" {run_single(n, 1):.4f}", end="")
    print()

if __name__ == "__main__":
    main()
