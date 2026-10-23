"""
service_manager.py
------------------
Stores service locations and provides category-based filtering.
"""


class ServiceManager:
    def __init__(self, services):
        self.services = list(services)

    def add_service(self, service):
        """Add a service to the main collection."""
        self.services.append(service)

    def get_by_category(self, category):
        """Return all services belonging to the given category."""
        return [
            service for service in self.services
            if service.category == category
        ]
