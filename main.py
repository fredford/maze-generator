import numpy as np
import maze_generator
import pygame, time


def main():
    pygame.init()
    board_width = 10
    board_height = 10
    screen = pygame.display.set_mode((board_width*50, board_height*50))
    maze = maze_generator.Maze(board_width, board_height)
    maze.print_maze()

    cells = maze.maze

    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()


    # Fill the background with white
    screen.fill((255, 255, 255))

    for i in range(len(cells)+1):
        pygame.draw.line(screen, (0,0,0), (0,i*50), (board_width*50,i*50))

    for j in range(len(cells[0])+1):
        pygame.draw.line(screen, (0,0,0), (j*50,0), (j*50,board_height*50))

    # Draw a solid blue circle in the center

    cell = cells[0][0]
    print(cell.walls)

    pos_x = 0
    pos_y = 0

    pygame.Rect(pos_x, pos_y, pos_x+50, pos_y+50)

    above = (pos_x + 5, pos_y, pos_x + 45, pos_y +45)
    below = (pos_y + 5, pos_y + 5, pos_x + 45, pos_y + 50)
    left = (pos_x, pos_y+5, pos_x+45, pos_y+45)
    right = (pos_x+5, pos_y+5, pos_x+50, pos_y+45)

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            cell = cells[i][j]

            for direction, value in cell.walls.items():

                if not value and direction == "above":
                    print('above')
                    pygame.draw.line(screen, (255,255,255), ((50*i)+1, (50*j)) , ((50*i)+49, (50*j)))
                if not value and direction == "below":
                    print('below')
                    pygame.draw.line(screen, (255,255,255), ((50*i)+1, (50*j)+50), ((50*i)+49, (50*j)+50))
                if not value and direction == "left":
                    print('left')
                    pygame.draw.line(screen, (255,255,255), ((50*i), (50*j)), ((50*i), (50*j)+49))
                if not value and direction == "right":
                    print('right')
                    pygame.draw.line(screen, (255,255,255), ((50*i)+50, (50*j)+1), ((50*i)+50, (50*j)+49))


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