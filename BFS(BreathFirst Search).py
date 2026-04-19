def open_area_5x5(maze, x, y):
    n = len(maze)

    for i in range(x-2, x+3):
        for j in range(y-2, y+3):
            if 0 <= i < n and 0 <= j < n:
                maze[i][j] = 0

def solve_maze_BFS():
    size = 100
    maze = generate_perfect_maze(size)

    start = (0, 0)
    goal = (size-1, size-1)

    open_area_5x5(maze, *start)
    open_area_5x5(maze, *goal)

    queue = [start]
    visited = set([start])
    parent = {}

    frames = []  
    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    # ---------------- BFS ----------------
    while queue:
        x, y = queue.pop(0)

        # save snapshot of current state
        frames.append((set(visited), (x, y)))

        if (x, y) == goal:
            break

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny) and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    # ---------------- reconstruct path ----------------
    path = []
    node = goal

    path = []

    if goal not in parent:
        print("No path found (BFS did not reach goal)")
        path = []
    else:
        node = goal
        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)
        path.reverse()

    path.append(start)
    path.reverse()

    return maze, frames, path, start, goal
