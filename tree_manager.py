"""
tree_manager.py
---------------
Builds and manages one KD-tree for each service category.
"""

from kdtree import KDTree
from data import CATEGORIES


class KDTreeManager:
    def __init__(self, service_manager):
        self.service_manager = service_manager
        self.trees = {}
        self.build_all()

    def build_all(self):
        """Build a KD-tree for every known category."""
        for category in CATEGORIES:
            group = self.service_manager.get_by_category(category)
            self.trees[category] = KDTree(group)

    def rebuild_category(self, category):
        """Rebuild only the tree affected by a newly added service."""
        group = self.service_manager.get_by_category(category)
        self.trees[category] = KDTree(group)

    def find_nearest(self, category, x, y, k=1):
        """Return the k nearest services in one category."""
        return self.trees[category].k_nearest((x, y), k)

    def find_nearest_any(self, x, y):
        """Return the nearest service in every nonempty category."""
        results = {}
        for category in CATEGORIES:
            service, dist = self.trees[category].nearest((x, y))
            if service is not None:
                results[category] = (service, dist)
        return results
