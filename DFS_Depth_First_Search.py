def solve_maze_DFS(maze, start, goal):

    stack = [start]
    visited = set([start])
    parent = {}

    frames = []

    rows, cols = len(maze), len(maze[0])

    def valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0

    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while stack:

        x, y = stack.pop()

        frames.append((set(visited), (x, y)))

        if (x, y) == goal:
            break

        for dx, dy in dirs:

            nx, ny = x+dx, y+dy

            if valid(nx, ny) and (nx, ny) not in visited:

                stack.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    if goal not in parent:
        return frames, None

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    path.reverse()

    return frames, path