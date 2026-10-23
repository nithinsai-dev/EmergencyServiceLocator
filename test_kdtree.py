"""
test_kdtree.py
--------------
Proves the KD-tree gives EXACTLY the same answers as brute force.
Run:  python test_kdtree.py
"""

import random
from math import inf
from kdtree import KDTree, Service, linear_k_nearest
from data import load_services


def random_services(n, seed):
    rnd = random.Random(seed)
    return [Service(f"S{i}", "Test", rnd.uniform(0, 100), rnd.uniform(0, 100))
            for i in range(n)]


def test_nearest_matches_linear():
    pts = random_services(500, seed=1)
    tree = KDTree(pts)
    rnd = random.Random(2)
    for _ in range(300):
        q = (rnd.uniform(0, 100), rnd.uniform(0, 100))
        kd_s, kd_d = tree.nearest(q)
        lin_s, lin_d = linear_k_nearest(pts, q, 1)[0]
        assert abs(kd_d - lin_d) < 1e-9
    print("PASS  nearest == linear on 300 random queries")


def test_k_nearest_matches_linear():
    pts = random_services(300, seed=3)
    tree = KDTree(pts)
    rnd = random.Random(4)
    for k in (1, 3, 5, 10):
        for _ in range(100):
            q = (rnd.uniform(0, 100), rnd.uniform(0, 100))
            kd = [round(d, 9) for _, d in tree.k_nearest(q, k)]
            lin = [round(d, 9) for _, d in linear_k_nearest(pts, q, k)]
            assert kd == lin
    print("PASS  k-nearest == linear for k = 1, 3, 5, 10")


def test_edge_cases():
    assert KDTree([]).nearest((5, 5)) == (None, inf)        # empty tree
    one = KDTree([Service("Only", "T", 10, 10)])
    assert one.nearest((90, 90))[0].name == "Only"           # single point
    pts = [Service("A", "T", 5, 5), Service("B", "T", 5, 5)]  # duplicates
    assert len(KDTree(pts).k_nearest((0, 0), 2)) == 2
    assert len(KDTree(pts).k_nearest((0, 0), 10)) == 2       # k > n
    print("PASS  edge cases (empty, single, duplicates, k > n)")


def test_balanced_height():
    import math
    tree = KDTree(random_services(1000, seed=5))
    assert tree.height() <= math.ceil(math.log2(1001)) + 1
    print(f"PASS  tree is balanced (1000 points -> height {tree.height()})")


def test_demo_dataset():
    services = load_services()
    hospitals = [s for s in services if s.category == "Hospital"]
    tree = KDTree(hospitals)
    s, d = tree.nearest((10, 78))
    assert s.name == "North Medical Center"
    print("PASS  demo dataset sanity check")


if __name__ == "__main__":
    test_nearest_matches_linear()
    test_k_nearest_matches_linear()
    test_edge_cases()
    test_balanced_height()
    test_demo_dataset()
    print("\nAll tests passed.")
