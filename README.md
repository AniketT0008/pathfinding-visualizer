## How It Works

The maze is represented as a 2D grid:
- 0 = path
- 1 = wall

BFS explores level by level using a queue to guarantee the shortest path.

DFS explores depth-first using a stack (LIFO), which may not find the shortest path.

A* uses a heuristic (Manhattan distance) to prioritize nodes closer to the goal, making it more efficient.
