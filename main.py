import numpy as np
import maze_generator
import pygame, time


def main():
    pygame.init()
    board_width = 10
    board_height = 10
    board_size = 90
    window_size = 600
    scale = window_size/board_size
    screen = pygame.display.set_mode((window_size, window_size))
    maze = maze_generator.Maze(board_size, board_size)
    maze.print_maze()

    cells = maze.maze

    pygame.display.set_caption("Maze")


    # Fill the background with white
    screen.fill((255, 255, 255))

    for i in range(len(cells)+1):
        pygame.draw.line(screen, (0,0,0), (0,i*scale), (window_size,i*scale))

    for j in range(len(cells[0])+1):
        pygame.draw.line(screen, (0,0,0), (j*scale,0), (j*scale,window_size))

    # Draw a solid blue circle in the center

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            cell = cells[i][j]

            for direction, value in cell.walls.items():

                if not value and direction == "above":
                    print('above')
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)) , ((scale*i)+scale, (scale*j)))
                if not value and direction == "below":
                    print('below')
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)+scale), ((scale*i)+scale, (scale*j)+scale))
                if not value and direction == "left":
                    print('left')
                    pygame.draw.line(screen, (255,255,255), ((scale*i), (scale*j)), ((scale*i), (scale*j)+scale))
                if not value and direction == "right":
                    print('right')
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+scale, (scale*j)+1), ((scale*i)+scale, (scale*j)+scale))


    # Flip the display
    pygame.display.flip()

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Done! Time to quit.
    pygame.quit()


main()