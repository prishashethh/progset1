#!/usr/bin/env python3
"""
Run the graph generator for all (n, dimension) cases and write each to a file.
Shows progress in the terminal.

Usage:
  python3 generate_all_graphs.py              # use default output dir and case set
  python3 generate_all_graphs.py --out DIR    # write files to DIR (default: generated_graphs)
  python3 generate_all_graphs.py --fast       # only fast/small n (default)
  python3 generate_all_graphs.py --all        # all n (can be slow and use a lot of disk)
"""

import os
import sys
import time
from typing import List, Tuple

from graph_generator import generate_and_write

# Default: fast set (smaller n) so runs and files stay manageable
FAST_COMPLETE_NS = [128, 256, 512, 1024, 2048]
FAST_HYPERCUBE_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384]
# Full set (optional with --all)
COMPLETE_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
HYPERCUBE_NS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]

DIMENSION_NAMES = {0: "0D", 1: "1D-hypercube", 2: "2D", 3: "3D", 4: "4D"}
DEFAULT_OUT_DIR = "generated_graphs"


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    use_fast = True
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("-h", "--help"):
            print(__doc__.strip())
            sys.exit(0)
        if args[i] == "--out" and i + 1 < len(args):
            out_dir = args[i + 1]
            i += 2
        elif args[i] == "--fast":
            use_fast = True
            i += 1
        elif args[i] == "--all":
            use_fast = False
            i += 1
        else:
            i += 1

    if use_fast:
        complete_ns = FAST_COMPLETE_NS
        hypercube_ns = FAST_HYPERCUBE_NS
    else:
        complete_ns = COMPLETE_NS
        hypercube_ns = HYPERCUBE_NS

    # Build list of (n, dim)
    cases: List[Tuple[int, int]] = []
    for dim in [0, 2, 3, 4]:
        for n in complete_ns:
            cases.append((n, dim))
    for n in hypercube_ns:
        cases.append((n, 1))

    os.makedirs(out_dir, exist_ok=True)
    total = len(cases)
    print("=" * 60)
    print(f"Generating {total} graphs -> {out_dir}/")
    print("=" * 60)

    t0 = time.time()
    for step, (n, dim) in enumerate(cases, 1):
        name = DIMENSION_NAMES.get(dim, f"dim{dim}")
        filename = f"graph_n{n}_dim{dim}.json"
        filepath = os.path.join(out_dir, filename)
        print(f"\n[{step}/{total}] n={n} dim={dim} ({name}) -> {filename}")
        print("-" * 50)
        try:
            generate_and_write(n, dim, filepath, seed=step - 1, verbose=True)
            print(f"  -> saved {filepath}")
        except Exception as e:
            print(f"  ERROR: {e}", flush=True)

    elapsed = time.time() - t0
    print("\n" + "=" * 60)
    print(f"Done. {total} graphs in {out_dir}/ in {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
