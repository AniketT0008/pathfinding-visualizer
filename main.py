from maze_generator import generate_perfect_maze, open_area_5x5
from visualizer import run_visual
from Astar import astar
from BFS_Breath_First_Search import solve_maze_BFS
from DFS_Depth_First_Search import solve_maze_DFS
import sys

sys.setrecursionlimit(10000)


def main():
    size = int(input("Enter maze size: "))

    maze = generate_perfect_maze(size)

    start = (0, 0)
    goal = (size - 1, size - 1)

    open_area_5x5(maze, *start)
    open_area_5x5(maze, *goal)

    print("\nChoose algorithm:")
    print("1 - A*")
    print("2 - BFS")
    print("3 - DFS")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        frames, path = astar(size, maze, start, goal)

    elif choice == "2":
        frames, path = solve_maze_BFS(maze, start, goal)

    elif choice == "3":
        frames, path = solve_maze_DFS(maze, start, goal)

    else:
        print("Invalid choice. Defaulting to A*.")
        frames, path = astar(size, maze, start, goal)

    run_visual(maze, frames, path, start, goal)


if __name__ == "__main__":
    main()
