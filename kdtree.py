"""
kdtree.py
---------
Core data structure of the project: a 2-D KD-Tree plus a linear-search
baseline used for comparison.

A KD-Tree (k-dimensional tree) is a binary search tree where every level
splits the points using a different coordinate:
    level 0 -> compare x,  level 1 -> compare y,  level 2 -> x, ...
"""

import heapq
import math


# ---------------------------------------------------------------- helpers
def euclidean(p, q):
    """Straight-line distance between two (x, y) points."""
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


class Service:
    """One service location (e.g. a hospital)."""

    def __init__(self, name, category, x, y):
        self.name = name
        self.category = category
        self.x = x
        self.y = y

    @property
    def point(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"{self.name} [{self.category}] ({self.x}, {self.y})"


class Node:
    """One node of the KD-tree."""

    def __init__(self, service, axis):
        self.service = service   # the location stored at this node
        self.axis = axis         # 0 = split on x, 1 = split on y
        self.left = None         # points with smaller coordinate on 'axis'
        self.right = None        # points with larger/equal coordinate


# ---------------------------------------------------------------- KD-Tree
class KDTree:
    def __init__(self, services):
        # Build the tree once from a list of Service objects.
        self.size = len(services)
        self.root = self._build(list(services), depth=0)

    # ---- Step 1: BUILD -------------------------------------------------
    def _build(self, services, depth):
        """Recursively build a balanced tree.

        Idea: sort by the current axis, pick the MEDIAN as the node,
        the left half goes to the left subtree, the right half to the right.
        Choosing the median keeps the tree balanced -> height ~ log2(n).
        """
        if not services:
            return None

        axis = depth % 2                                  # alternate x, y
        services.sort(key=lambda s: s.point[axis])
        mid = len(services) // 2

        node = Node(services[mid], axis)
        node.left = self._build(services[:mid], depth + 1)
        node.right = self._build(services[mid + 1:], depth + 1)
        return node

    # ---- Step 2: NEAREST NEIGHBOUR ------------------------------------
    def nearest(self, target):
        """Return (service, distance) of the closest point to 'target'."""
        result = self.k_nearest(target, 1)
        return result[0] if result else (None, None)

    # ---- Step 3: K NEAREST NEIGHBOURS ---------------------------------
    def k_nearest(self, target, k=1):
        """Return the k closest services as [(service, distance), ...]
        sorted from nearest to farthest.

        We keep a 'best list' of up to k candidates found so far.
        We use a max-heap (distances stored negative) so the WORST of the
        k candidates is always on top and easy to replace.
        """
        best = []            # heap items: (-distance, counter, service)
        counter = [0]        # tie-breaker + counts how many nodes we visit

        def search(node):
            if node is None:
                return

            # 1) Consider the point stored in this node.
            d = euclidean(target, node.service.point)
            counter[0] += 1
            if len(best) < k:
                heapq.heappush(best, (-d, counter[0], node.service))
            elif d < -best[0][0]:
                heapq.heapreplace(best, (-d, counter[0], node.service))

            # 2) Decide which side of the splitting line the target is on.
            diff = target[node.axis] - node.service.point[node.axis]
            near_side, far_side = (node.left, node.right) if diff < 0 \
                else (node.right, node.left)

            # 3) Always search the near side first.
            search(near_side)

            # 4) PRUNING: only visit the far side if the splitting line is
            #    closer than our current worst candidate (or we have < k).
            #    Otherwise nothing on the far side can possibly be better.
            if len(best) < k or abs(diff) < -best[0][0]:
                search(far_side)

        search(self.root)
        self.nodes_visited = counter[0]   # shows how much work pruning saved
        return [(s, -nd) for nd, _, s in sorted(best, reverse=True)]

    # ---- Extra: tree height (useful to show it is balanced) -----------
    def height(self):
        def h(node):
            return 0 if node is None else 1 + max(h(node.left), h(node.right))
        return h(self.root)

    # ---- Extra: print the tree (useful for demo) ----------------------
    def print_tree(self, node="root", indent=0):
        if node == "root":
            node = self.root
        if node is None:
            return
        self.print_tree(node.right, indent + 1)
        axis = "x" if node.axis == 0 else "y"
        print("    " * indent + f"{node.service.name} (split on {axis})")
        self.print_tree(node.left, indent + 1)


# ---------------------------------------------------------------- baseline
def linear_k_nearest(services, target, k=1):
    """Traditional method: measure the distance to EVERY service. O(n)."""
    scored = [(s, euclidean(target, s.point)) for s in services]
    scored.sort(key=lambda pair: pair[1])
    return scored[:k]
