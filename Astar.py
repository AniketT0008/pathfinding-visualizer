import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(size, maze, start, goal):

    rows, cols = len(maze), len(maze[0])

    pq = [(0, start)]

    g_cost = {start: 0}
    came_from = {}

    closed = set()
    frames = []

    while pq:

        _, current = heapq.heappop(pq)

        if current in closed:
            continue
        closed.add(current)

        frames.append((set(closed), current))

        if current == goal:
            break

        x, y = current

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:

            nx, ny = x+dx, y+dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:

                new_g = g_cost[current] + 1

                if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:

                    g_cost[(nx, ny)] = new_g
                    f = new_g + heuristic((nx, ny), goal)

                    heapq.heappush(pq, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

    # path
    if goal not in came_from:
        return frames, None

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = came_from[node]

    path.append(start)
    path.reverse()

    return frames, path