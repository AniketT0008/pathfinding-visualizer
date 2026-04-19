from maze_generator import generate_perfect_maze
from visualizer import run_visual
import sys
from BFS_Breath_First_Search import solve_maze_BFS
from DFS_Depth_First_Search import solve_maze_DFS
sys.setrecursionlimit(10000)


run_visual(solve_maze())
