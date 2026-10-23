"""
nearest_service_system.py
-------------------------
Coordinates service storage and KD-tree search operations.
"""

from service_manager import ServiceManager
from tree_manager import KDTreeManager


class NearestServiceSystem:
    def __init__(self, services):
        self.service_manager = ServiceManager(services)
        self.tree_manager = KDTreeManager(self.service_manager)

    @property
    def services(self):
        """Expose the full service list for existing menu code."""
        return self.service_manager.services

    @property
    def trees(self):
        """Expose the category-to-tree dictionary for display/comparison."""
        return self.tree_manager.trees

    def add_service(self, service):
        """Add a service and rebuild its category's KD-tree."""
        self.service_manager.add_service(service)
        self.tree_manager.rebuild_category(service.category)

    def find_nearest(self, category, x, y, k=1):
        return self.tree_manager.find_nearest(category, x, y, k)

    def find_nearest_any(self, x, y):
        return self.tree_manager.find_nearest_any(x, y)
