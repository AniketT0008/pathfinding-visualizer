"""
Shared tunables for the pathfinding visualization robot.

Edit these once for your floor / battery / gearbox ratios.
"""

# Maze
DEFAULT_MAZE_SIZE = 21  # odd sizes work best with the DFS carver

# Visualizer
CELL_PX = 12
ANIMATION_FPS = 60

# Robot drive timing (milliseconds) — tune on a clear floor
CELL_MS = 450   # one grid step forward
TURN_MS = 320   # 90° pivot

# Set True to always print commands without sending (safe default until WiFi works)
DEFAULT_DRY_RUN = True
