def run_visual(maze, frames, path, start, goal):

    import pygame
    clock = pygame.time.Clock()

    CELL = 7

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BLUE  = (0,0,255)
    GREEN = (0,255,0)
    RED   = (255,0,0)
    ORANGE = (255,165,0)

    pygame.init()

    rows, cols = len(maze), len(maze[0])
    screen = pygame.display.set_mode((cols*CELL, rows*CELL))


    path_set = set(path)

    step = 0
    running = True
    show_path = False

    while running:

        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # BFS ANIMATION
        if step < len(frames):
            visited, current = frames[step]
            step += 1
        else:
            visited, current = frames[-1]
            show_path = True  

        # DRAW GRID
        for i in range(rows):
            for j in range(cols):

                # walls (thinner look via softer color)
                if maze[i][j] == 1:
                    color = BLACK
                else:
                    color = WHITE

                # visited nodes
                if (i,j) in visited:
                    color = BLUE

                # current BFS node
                if (i,j) == current:
                    color = ORANGE

                # start / goal
                if (i,j) == start or (i,j) == goal:
                    color = RED

                # FINAL PATH ONLY AFTER BFS DONE
                if show_path and (i,j) in path_set:
                    color = GREEN

                pygame.draw.rect(
                    screen,
                    color,
                    (j*CELL, i*CELL, CELL-1, CELL-1)  # 🔥 thin grid effect
                )

        pygame.display.update()
        clock.tick(15)

    pygame.quit()