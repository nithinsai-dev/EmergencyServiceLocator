"""
data.py
-------
Sample service locations and category definitions.
Coordinates are illustrative 2D points in the range 0-100.
"""

import random

from kdtree import Service

CATEGORIES = ["Hospital", "ATM", "Pharmacy", "Police"]

# Coordinate range used by the menu and by the random generator.
COORD_MIN = 0
COORD_MAX = 100


def load_services():
    """Return the initial list of service locations."""
    return [
        Service("City Hospital", "Hospital", 20, 25),
        Service("General Hospital", "Hospital", 65, 70),
        Service("North Medical Center", "Hospital", 42, 80),
        Service("Community Hospital", "Hospital", 78, 30),

        Service("Central ATM", "ATM", 15, 20),
        Service("Mall ATM", "ATM", 55, 45),
        Service("Station ATM", "ATM", 82, 75),
        Service("Market ATM", "ATM", 35, 60),

        Service("Care Pharmacy", "Pharmacy", 25, 35),
        Service("HealthPlus Pharmacy", "Pharmacy", 60, 65),
        Service("Green Cross Pharmacy", "Pharmacy", 75, 20),
        Service("Town Pharmacy", "Pharmacy", 40, 50),

        Service("Central Police Station", "Police", 10, 80),
        Service("East Police Station", "Police", 70, 55),
        Service("West Police Station", "Police", 30, 15),
        Service("South Police Station", "Police", 85, 35),
    ]


def generate_services(n, category="Hospital", seed=None,
                      low=COORD_MIN, high=COORD_MAX):
    """
    Return n randomly placed services of one category.

    Use a fixed seed for reproducible benchmarks and tests.
    """
    rng = random.Random(seed)
    return [
        Service(f"{category} #{i}", category,
                rng.uniform(low, high), rng.uniform(low, high))
        for i in range(n)
    ]


def generate_all_categories(n_per_category, seed=None):
    """Return a mixed list with n_per_category random services per category."""
    services = []
    for offset, category in enumerate(CATEGORIES):
        category_seed = None if seed is None else seed + offset
        services.extend(generate_services(n_per_category, category, category_seed))
    return services


def generate_query_points(count, seed=None, low=COORD_MIN, high=COORD_MAX):
    """Return a list of random (x, y) query points."""
    rng = random.Random(seed)
    return [(rng.uniform(low, high), rng.uniform(low, high))
            for _ in range(count)]
