import pygame
import config


def run_visual(maze, frames, path, start, goal):
    """Animate search expansion, then draw the final path."""
    clock = pygame.time.Clock()
    CELL = config.CELL_PX

    WHITE = (245, 245, 245)
    BLACK = (20, 20, 20)
    BLUE = (66, 135, 245)
    GREEN = (46, 204, 113)
    RED = (231, 76, 60)
    ORANGE = (243, 156, 18)
    PATH_HEAD = (155, 89, 182)

    pygame.init()
    rows, cols = len(maze), len(maze[0])
    screen = pygame.display.set_mode((cols * CELL, rows * CELL))
    pygame.display.set_caption("Pathfinding Visualizer + Robot")

    path_list = list(path) if path else []
    path_set = set(path_list)

    step = 0
    running = True
    show_path = False
    path_idx = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(WHITE)

        if frames and step < len(frames):
            visited, current = frames[step]
            step += 1
        elif frames:
            visited, current = frames[-1]
            show_path = True
        else:
            visited, current = set(), start
            show_path = True

        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == 1:
                    color = BLACK
                else:
                    color = WHITE

                if (i, j) in visited:
                    color = BLUE

                if (i, j) == current:
                    color = ORANGE

                if show_path and (i, j) in path_set:
                    color = GREEN

                if (i, j) == start or (i, j) == goal:
                    color = RED

                # Animate a "robot" cursor along the solved path after search finishes
                if show_path and path_list and (i, j) == path_list[min(path_idx, len(path_list) - 1)]:
                    color = PATH_HEAD

                pygame.draw.rect(
                    screen,
                    color,
                    (j * CELL, i * CELL, CELL - 1, CELL - 1),
                )

        if show_path and path_list:
            path_idx = min(path_idx + 1, len(path_list) - 1)

        pygame.display.update()
        clock.tick(config.ANIMATION_FPS)

        # Auto-close shortly after path cursor finishes
        if show_path and path_list and path_idx >= len(path_list) - 1:
            # keep window open until user closes, but don't spin forever at 60fps burn
            clock.tick(30)

    pygame.quit()
