# Pathfinding Visualizer

A Python-based visualizer that generates mazes and solves them using BFS, DFS, and A* algorithms with real-time animation.

## Features

- Random maze generation (custom size)
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- A* Search (heuristic-based)
- Step-by-step visualization of algorithm traversal
- Displays the final optimal path after completion
- Interactive algorithm selection at runtime

## How It Works

The maze is represented as a 2D grid:
- `0` = path
- `1` = wall

### Algorithms

- **BFS** explores level-by-level using a queue and guarantees the shortest path.
- **DFS** explores depth-first using a stack (LIFO) and does not guarantee the shortest path.
- **A\*** uses a heuristic (Manhattan distance) to prioritize nodes closer to the goal, making it more efficient.

## How to Run

1. Install dependencies:
   pygame
   numpy
   opencv-python
2. Run:
   python main.py

### Input
  Enter maze size (e.g., 50, 100)
  Choose algorithm:
    A*
    BFS
    DFS
### Project Structure
main.py                        # Entry point (user interaction + control flow)
maze_generator.py              # Generates random maze grid
visualizer.py                  # Handles animation and rendering
Astar.py                       # A* pathfinding implementation
BFS_Breath_First_Search.py     # BFS implementation
DFS_Depth_First_Search.py      # DFS implementation

###Example Input and Output

Input:
<img width="425" height="121" alt="Demo" src="https://github.com/user-attachments/assets/cbf969f4-328d-4af6-9245-ccb63ec4dba7" />


Output:
<img width="376" height="398" alt="image" src="https://github.com/user-attachments/assets/ad86dcae-fc1b-4571-b1f9-ab6bcfaa548b" />
