# 🕸️ Maze-Pathfinding-Visualizer-Benchmarker
A Python, Tkinter graphic application to generate mazes with various maze-generator algorithms and benchmark the execution time of various pathfinding algorithms.  

## 📚 What I learned

- **Pathfinding & Graph Algorithms** : Taught me how to implement and visually compare Depth-First Search (DFS) and Dijkstra's algorithm to find the shortest path in a generated grid.
  
- **Object-Oriented Programming (OOP)** : Structured the project using custom classes (`cellule`, `labyrinthe`) and operator overloading (`__add__`, `__eq__` in `coord`) to cleanly manage 2D movements and grid states.
  
- **GUI & Event-Driven Programming** : Used `tkinter` to build an interactive canvas, manage real-time visual updates during algorithm execution, and bind user mouse clicks to place dynamic start/end points.
  
- **Custom Data Structures** : Built and managed a custom Stack (LIFO) for the DFS maze generation, and mapped the grid into a dictionary-based adjacency list for Dijkstra's evaluation.
  
- **Algorithm Benchmarking** : Implemented a timing system to track, calculate, and display the exact execution speed of each pathfinding method to compare their efficiency.
  
