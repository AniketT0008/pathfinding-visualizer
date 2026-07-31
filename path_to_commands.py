"""
Convert a grid path [(row, col), ...] into timed motor commands.

Coordinate convention (matches the visualizer maze):
  - row increases DOWN the screen
  - col increases RIGHT
  - robot starts facing EAST (increasing col), at path[0]
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Cell = Tuple[int, int]

# Facing vectors: (d_row, d_col)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
NORTH = (-1, 0)
FACINGS = [EAST, SOUTH, WEST, NORTH]  # clockwise order
FACING_NAME = {
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
    NORTH: "N",
}


def _turn_commands(current: Tuple[int, int], target: Tuple[int, int], turn_ms: int) -> List[str]:
    """Return LEFT:/RIGHT: timed pivots to rotate from current facing to target."""
    cur_i = FACINGS.index(current)
    tgt_i = FACINGS.index(target)
    delta = (tgt_i - cur_i) % 4  # 0 none, 1 right, 2 about-face, 3 left

    if delta == 0:
        return []
    if delta == 1:
        return [f"RIGHT:{turn_ms}"]
    if delta == 3:
        return [f"LEFT:{turn_ms}"]
    # 180° — two rights (or two lefts); rights keep consistent bias
    return [f"RIGHT:{turn_ms}", f"RIGHT:{turn_ms}"]


def path_to_commands(
    path: Sequence[Cell],
    *,
    cell_ms: int = 450,
    turn_ms: int = 320,
    start_facing: Tuple[int, int] = EAST,
) -> List[str]:
    """
    Turn a cell path into ESP32 timed commands.

    cell_ms  — how long FORWARD lasts for one grid step (tune for your motors)
    turn_ms  — how long a 90° pivot lasts (tune until turns look square)
    """
    if not path or len(path) < 2:
        return []

    facing = start_facing
    cmds: List[str] = []

    for a, b in zip(path, path[1:]):
        dr = b[0] - a[0]
        dc = b[1] - a[1]

        if abs(dr) + abs(dc) != 1:
            raise ValueError(
                f"Path must be 4-connected unit steps; got {a} -> {b}"
            )

        desired = (dr, dc)
        cmds.extend(_turn_commands(facing, desired, turn_ms))
        facing = desired
        cmds.append(f"FORWARD:{cell_ms}")

    cmds.append("STOP")
    return cmds


def summarize_path(path: Iterable[Cell]) -> str:
    cells = list(path)
    if not cells:
        return "empty path"
    return f"{len(cells)} cells from {cells[0]} to {cells[-1]}"
