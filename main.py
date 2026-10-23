"""
main.py
-------
Menu-driven Nearest Service Location System.
"""

from kdtree import Service, linear_k_nearest
from data import load_services, CATEGORIES
from nearest_service_system import NearestServiceSystem


def read_number(prompt, low=0, high=100):
    while True:
        try:
            value = float(input(prompt))
            if low <= value <= high:
                return value
            print(f"  Please enter a value between {low} and {high}.")
        except ValueError:
            print("  Invalid number, try again.")


def choose_category():
    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"  {i}. {category}")

    while True:
        choice = input(f"Choose category (1-{len(CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("  Invalid choice.")


def show_results(results):
    if not results:
        print("  No services found in this category.")
        return

    for rank, (service, dist) in enumerate(results, 1):
        print(
            f"  {rank}. {service.name:<26} at "
            f"({service.x}, {service.y})   distance = {dist:.2f}"
        )


def main():
    system = NearestServiceSystem(load_services())

    while True:
        print("\n===== NEAREST SERVICE LOCATION SYSTEM =====")
        print("1. Find nearest service (by category)")
        print("2. Find k nearest services (by category)")
        print("3. Emergency overview (nearest of every category)")
        print("4. Add a new service location")
        print("5. Show KD-tree structure (for one category)")
        print("6. Compare KD-tree vs linear search (one query)")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            category = choose_category()
            x = read_number("Your x (0-100): ")
            y = read_number("Your y (0-100): ")
            print(f"\nNearest {category}:")
            show_results(system.find_nearest(category, x, y, 1))

        elif choice == "2":
            category = choose_category()
            x = read_number("Your x (0-100): ")
            y = read_number("Your y (0-100): ")
            k = int(read_number("How many results (1-5)? ", 1, 5))
            print(f"\n{k} nearest {category}(s):")
            show_results(system.find_nearest(category, x, y, k))

        elif choice == "3":
            x = read_number("Your x (0-100): ")
            y = read_number("Your y (0-100): ")
            print("\nNearest service in each category:")
            results = system.find_nearest_any(x, y)
            for category, (service, dist) in results.items():
                print(
                    f"  {category:<15} -> {service.name:<26} "
                    f"distance = {dist:.2f}"
                )

        elif choice == "4":
            name = input("Name: ").strip()
            category = choose_category()
            x = read_number("x (0-100): ")
            y = read_number("y (0-100): ")

            if not name:
                print("  Service name cannot be empty.")
                continue

            system.add_service(Service(name, category, x, y))
            print(f"  Added '{name}'. {category} tree rebuilt.")

        elif choice == "5":
            category = choose_category()
            tree = system.trees[category]
            print(
                f"\n{category} tree. Height = {tree.height()}"
            )
            tree.print_tree()

        elif choice == "6":
            category = choose_category()
            x = read_number("Your x (0-100): ")
            y = read_number("Your y (0-100): ")

            tree = system.trees[category]
            group = system.service_manager.get_by_category(category)

            kd = tree.k_nearest((x, y), 1)
            linear = linear_k_nearest(group, (x, y), 1)

            if not kd or not linear:
                print("  No services available in this category.")
                continue

            print(
                f"\n  KD-tree answer : {kd[0][0].name} "
                f"(visited {tree.nodes_visited} of {len(group)} nodes)"
            )
            print(
                f"  Linear answer  : {linear[0][0].name} "
                f"(checked {len(group)} of {len(group)} points)"
            )
            print("  Same result?   :", kd[0][0] is linear[0][0])

        elif choice == "0":
            print("Stay safe. Goodbye!")
            break

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
