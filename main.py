from maze_generator import generate_perfect_maze, open_area_5x5
from visualizer import run_visual
from Astar import astar
from BFS_Breath_First_Search import solve_maze_BFS
from DFS_Depth_First_Search import solve_maze_DFS
from path_to_commands import path_to_commands, summarize_path
from robot_client import execute_commands
import config
import sys

sys.setrecursionlimit(10000)


def _pick_size() -> int:
    raw = input(f"Enter maze size [{config.DEFAULT_MAZE_SIZE}]: ").strip()
    if not raw:
        return config.DEFAULT_MAZE_SIZE
    size = int(raw)
    if size < 5:
        raise ValueError("Maze size must be at least 5")
    return size


def _pick_algorithm(size, maze, start, goal):
    print("\nChoose algorithm:")
    print("1 - A*")
    print("2 - BFS")
    print("3 - DFS")
    choice = input("Enter choice [1]: ").strip() or "1"

    if choice == "2":
        return solve_maze_BFS(maze, start, goal), "BFS"
    if choice == "3":
        return solve_maze_DFS(maze, start, goal), "DFS"
    return astar(size, maze, start, goal), "A*"


def _ask_drive_robot(path) -> None:
    if not path:
        print("No path found — nothing to drive.")
        return

    print(f"\nPath ready: {summarize_path(path)}")
    print("Drive the physical robot along this path? (ESP32-S3 + L298N)")
    print("  n = skip")
    print("  d = dry-run (print commands only)")
    print("  y = send to ESP32 over WiFi")
    ans = input("Choice [n]: ").strip().lower() or "n"

    if ans not in {"y", "d"}:
        print("Skipping robot drive.")
        return

    cmds = path_to_commands(
        path,
        cell_ms=config.CELL_MS,
        turn_ms=config.TURN_MS,
    )
    dry = ans == "d" or config.DEFAULT_DRY_RUN and ans != "y"
    if ans == "y":
        dry = False

    execute_commands(cmds, dry_run=dry, stop_at_end=False)


def main():
    size = _pick_size()

    maze = generate_perfect_maze(size)
    start = (0, 0)
    goal = (size - 1, size - 1)

    open_area_5x5(maze, *start)
    open_area_5x5(maze, *goal)
    # Guarantee start/goal cells are open even on tiny mazes
    maze[start[0]][start[1]] = 0
    maze[goal[0]][goal[1]] = 0

    (frames, path), name = _pick_algorithm(size, maze, start, goal)
    print(f"Running {name}… visited frames={len(frames)}, path={summarize_path(path) if path else 'NONE'}")

    # Animate search, then highlight path (and optional live cursor along path)
    run_visual(maze, frames, path or [], start, goal)

    _ask_drive_robot(path)


if __name__ == "__main__":
    main()
