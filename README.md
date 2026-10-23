# Nearest Emergency Service Location System Using KD-Trees

## 1. Project Overview

The **Nearest Emergency Service Location System** is a Python-based application designed to help users locate the nearest essential services, such as hospitals, petrol stations, ATMs, and pharmacies, based on their current coordinates.

The system uses a **K-Dimensional Tree (KD-Tree)**, a space-partitioning data structure that organizes service locations using their two-dimensional coordinates. It calculates Euclidean distances between the user's location and available services to identify the nearest locations efficiently.

Unlike traditional linear search, which checks every service location for each query, a KD-Tree can eliminate parts of the search space that cannot contain a closer result. This can improve search efficiency for suitable datasets.

The application also supports category-based searching, finding multiple nearest locations, displaying the KD-Tree structure, adding new service locations, and comparing KD-Tree search performance with linear search.

## 2. Problem Statement

Finding the nearest essential service location can become inefficient when a large number of locations must be searched repeatedly. Traditional linear search calculates the distance to every location for each query, resulting in linear query time.

The objective of this project is to implement an efficient nearest-service search system using KD-Trees. By organizing service locations according to their spatial coordinates, the system aims to reduce unnecessary distance calculations and improve query performance.

## 3. Objectives

- Implement a KD-Tree to organize two-dimensional service locations.
- Find the nearest service based on a user's coordinates.
- Support category-based searches for specific service types.
- Retrieve the k nearest locations within a selected category.
- Provide an emergency overview showing the nearest service in each category.
- Allow new service locations to be added dynamically.
- Display the structure and height of a KD-Tree.
- Compare KD-Tree search with traditional linear search.
- Understand the practical application of tree-based data structures in spatial searching.

## 4. Technologies Used

| Component              | Technology                    |
| ---------------------- | ----------------------------- |
| Programming language   | Python 3                      |
| Primary data structure | KD-Tree                       |
| Distance calculation   | Euclidean distance            |
| Data organization      | Python lists and dictionaries |
| User interface         | Command-line menu             |
| Data source            | Local sample dataset          |

## 5. Data Structure Used: KD-Tree

A KD-Tree, or K-Dimensional Tree, is a binary tree used to organize points in a k-dimensional space.

In this project, each service location is represented by a point `(x, y)`, where `x` and `y` represent its coordinates.

Each KD-Tree node stores a service location and references to its left and right child nodes. The tree alternates between splitting points by their x-coordinate and y-coordinate.

### 5.1 How It Works

1. The first level compares x-coordinates.
2. The next level compares y-coordinates.
3. The process continues alternating between the two dimensions.
4. During a nearest-neighbor query, the algorithm explores promising branches and examines the opposite branch when it may contain a closer point.

### 5.2 Why Use a KD-Tree?

A KD-Tree is suitable for this problem because service locations are represented by two-dimensional coordinates. It allows the search algorithm to use spatial information rather than checking every location unconditionally.

The project creates **one KD-Tree per service category**. For example, a hospital search examines the hospital tree rather than searching through ATMs, pharmacies, and petrol stations.

## 6. Distance Calculation

The system uses Euclidean distance to calculate the straight-line distance between the user's location and a service location.

For a user at `(x1, y1)` and a service at `(x2, y2)`, the distance is:

d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

The service with the smallest distance is considered the nearest service.

**Note:** The coordinates represent a simplified two-dimensional model. The calculated distance is not necessarily the actual road distance or travel time.

## 7. System Architecture

The application is organized into three main components.

### 7.1 Data Layer — `data.py`

Responsible for providing the sample service locations and the available service categories.

### 7.2 KD-Tree Layer — `kdtree.py`

Responsible for the KD-Tree data structure, spatial search operations, and linear-search comparison.

Responsibilities include:

- Representing service locations using a `Service` class.
- Constructing and maintaining the KD-Tree.
- Finding the nearest service.
- Finding the k nearest services.
- Calculating distances.
- Implementing linear nearest-neighbor search for comparison.
- Displaying the tree structure and its height.

### 7.3 Application Layer — `main.py`

Responsible for connecting the data and KD-Tree components and providing the menu-driven interface.

It manages category-wise trees, validates user input, displays search results, adds new locations, and provides the performance comparison option.

## 8. Features

### 8.1 Find the Nearest Service

Allows the user to select a category and enter their x and y coordinates. The system returns the nearest service in that category.

### 8.2 Find K Nearest Services

Allows the user to specify the number of nearby services to retrieve, from 1 to 5. The results are displayed in ascending order of distance.

### 8.3 Emergency Overview

Displays the nearest available service in every category for a given user location. This is useful when a user wants to identify nearby essential services without performing separate searches manually.

### 8.4 Add a New Service Location

Allows the user to enter the service name, category, and coordinates. The application updates its service collection and rebuilds the KD-Tree associated with that category.

### 8.5 Display KD-Tree Structure

Displays the structure and height of the selected category's KD-Tree. This helps demonstrate how service locations are organized within the tree.

### 8.6 Compare KD-Tree and Linear Search

Runs the same nearest-neighbor query using both methods and displays their results.

The KD-Tree search reports the number of nodes visited, while linear search checks every service in the selected category. The application also checks whether both methods return the same service object.

## 9. Algorithmic Approach

### 9.1 KD-Tree Construction

1. Collect the service locations belonging to a category.
2. Select the coordinate dimension for the current tree depth.
3. Organize the points using the selected coordinate.
4. Select a splitting point and recursively construct the left and right subtrees.
5. Repeat until all points have been placed in the tree.

### 9.2 Nearest-Neighbor Search

1. Start from the root node.
2. Calculate the distance from the query point to the current service.
3. Update the best candidate if a closer service is found.
4. Visit the subtree on the side of the splitting plane containing the query point.
5. Check whether the opposite subtree could contain a closer service.
6. Explore the opposite subtree if necessary.
7. Return the service with the minimum distance found.

### 9.3 Linear Search

1. Iterate through every service in the selected category.
2. Calculate its distance from the query point.
3. Maintain the closest service or the k closest services.
4. Return the results in ascending order of distance.

## 10. Time and Space Complexity

Let:

- `n` be the number of services in a category.
- `k` be the number of nearest services requested.

| Operation                                       | Typical or expected complexity                            | Worst case                                           |
| ----------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| KD-Tree construction                            | O(n log n) with median-based construction                 | Depends on the construction algorithm                |
| Nearest-neighbor query                          | Often O(log n) for favorable spatial distributions        | O(n)                                                 |
| K-nearest-neighbor query                        | Often sublinear, depending on the data and implementation | O(n log k) with a suitable bounded-size heap         |
| Linear nearest-neighbor search                  | O(n)                                                      | O(n)                                                 |
| Adding a service using category-tree rebuilding | Depends on rebuilding algorithm                           | Includes the cost of rebuilding that category's tree |
| KD-Tree storage                                 | O(n)                                                      | O(n)                                                 |

The exact complexity depends on how the KD-Tree is constructed and how nearest-neighbor and k-nearest-neighbor searches are implemented. KD-Tree queries are not guaranteed to take O(log n) time for every dataset.

## 11. How to Run the Project

### 11.1 Prerequisites

- Python 3 installed on your system.
- A code editor or terminal.
- All three Python files placed in the same project directory.

### 11.2 Steps to Execute

**Step 1: Open the project directory.**

```bash
cd nearest-service-location-system
```
