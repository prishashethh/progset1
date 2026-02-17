import sys
import random

from graph_generator import generate_pruned_edges
from mst import mst_weight


def main():
    # lol doing the terminal stuff they wanted us to do 
    # ./randmst 0 numpoints numtrials dimension
    if len(sys.argv) != 5:
        print("Usage: ./randmst 0 numpoints numtrials dimension", file=sys.stderr)
        sys.exit(1)

    flag = int(sys.argv[1])         
    numpoints = int(sys.argv[2])
    numtrials = int(sys.argv[3])
    dimension = int(sys.argv[4])

    # autograder fixes so that it can rerun 
    base_seed = random.SystemRandom().randrange(1 << 30)

    total_weight = 0.0
    for t in range(numtrials):
        # independent randomness per trial
        graph = generate_pruned_edges(numpoints, dimension, seed=base_seed + t, grace=2.0)
        total_weight += mst_weight(numpoints, graph, dimension)

    avg = total_weight / numtrials
    print(f"{avg} {numpoints} {numtrials} {dimension}")


if __name__ == "__main__":
    main()