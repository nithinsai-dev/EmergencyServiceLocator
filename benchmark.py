"""
benchmark.py
------------
Compares KD-tree search against linear search as the number of locations
grows. This is the evidence for the project objective:
"improve search efficiency compared with traditional linear search".

Run:  python benchmark.py
"""

import random
import time
from kdtree import KDTree, Service, linear_k_nearest


def make_points(n, seed=0):
    rnd = random.Random(seed)
    return [Service(f"S{i}", "Test", rnd.uniform(0, 1000), rnd.uniform(0, 1000))
            for i in range(n)]


def main():
    sizes = [100, 1_000, 10_000, 50_000]
    queries = 200
    rnd = random.Random(99)
    qs = [(rnd.uniform(0, 1000), rnd.uniform(0, 1000)) for _ in range(queries)]

    print(f"{'Points':>8} | {'Build (ms)':>10} | {'Linear (ms/q)':>13} | "
          f"{'KD-tree (ms/q)':>14} | {'Speed-up':>8} | {'Nodes visited':>13}")
    print("-" * 83)

    for n in sizes:
        pts = make_points(n)

        t0 = time.perf_counter()
        tree = KDTree(pts)
        build_ms = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for q in qs:
            linear_k_nearest(pts, q, 1)
        lin_ms = (time.perf_counter() - t0) * 1000 / queries

        visited_total = 0
        t0 = time.perf_counter()
        for q in qs:
            tree.k_nearest(q, 1)
            visited_total += tree.nodes_visited
        kd_ms = (time.perf_counter() - t0) * 1000 / queries

        print(f"{n:>8} | {build_ms:>10.1f} | {lin_ms:>13.4f} | "
              f"{kd_ms:>14.4f} | {lin_ms / kd_ms:>7.1f}x | "
              f"{visited_total / queries:>13.1f}")

    print("\nLinear search checks every point (O(n)).")
    print("KD-tree prunes whole regions (about O(log n) on average).")


if __name__ == "__main__":
    main()
