import random
import sys
sys.setrecursionlimit(10000)

def open_area_5x5(maze, x, y):
    n = len(maze)

    for i in range(x-2, x+3):
        for j in range(y-2, y+3):
            if 0 <= i < n and 0 <= j < n:
                maze[i][j] = 0

def generate_perfect_maze(n=100, start=(0,0), goal=(99,99)):

    maze = [[1 for _ in range(n)] for _ in range(n)]

    loop_chance=0.15

    def carve(x, y):
        maze[x][y] = 0

        dirs = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            if 1 <= nx < n-1 and 1 <= ny < n-1 and maze[nx][ny] == 1:
                maze[x + dx//2][y + dy//2] = 0
                carve(nx, ny)

    # Step 1: DFS maze (valid structure)
    carve(1, 1)

    # Step 2: ADD LOOPS (fake paths properly)
    for i in range(1, n-1):
        for j in range(1, n-1):

            if maze[i][j] == 1 and random.random() < loop_chance:

                # open wall between neighbors (safe carving)
                if i > 1:
                    maze[i][j] = 0
                if j > 1:
                    maze[i][j] = 0

    return maze