def solve_maze_BFS(maze, start, goal):

    if maze[start[0]][start[1]] == 1 or maze[goal[0]][goal[1]] == 1:
        return [], None
    if start == goal:
        return [(set([start]), start)], [start]

    queue = [start]
    visited = set([start])
    parent = {}

    frames = []

    rows, cols = len(maze), len(maze[0])

    def valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0

    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while queue:

        x, y = queue.pop(0)

        frames.append((set(visited), (x, y)))

        if (x, y) == goal:
            break

        for dx, dy in dirs:

            nx, ny = x+dx, y+dy

            if valid(nx, ny) and (nx, ny) not in visited:

                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    # reconstruct
    if goal not in parent and goal != start:
        return frames, None

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    path.reverse()

    return frames, path