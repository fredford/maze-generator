import maze_generator
import pygame, time
import maze as mg
#from window import Window
import a_star as astar


def main():
    pygame.init()
    board_size = 20
    window_size = 600
    scale = window_size/board_size
    screen = pygame.display.set_mode((window_size, window_size))
    maze = mg.Maze(board_size, board_size)

    cells = maze.maze

    a_star = astar.A_star(maze)


    pygame.display.set_caption("Maze")

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0,0,255), (maze.start.x*scale, maze.start.y*scale, scale, scale))
    pygame.draw.rect(screen, (255,0,0), (maze.end.x*scale, maze.end.y*scale, scale, scale))

    for i in range(len(cells)+1):
        pygame.draw.line(screen, (0,0,0), (0,i*scale), (window_size,i*scale))

    for j in range(len(cells[0])+1):
        pygame.draw.line(screen, (0,0,0), (j*scale,0), (j*scale,window_size))

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            cell = cells[i][j]

            for direction, value in cell.walls.items():

                if not value and direction == "above":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)) , ((scale*i)+scale-1, (scale*j)))
                if not value and direction == "below":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)+scale), ((scale*i)+scale-1, (scale*j)+scale))
                if not value and direction == "left":
                    pygame.draw.line(screen, (255,255,255), ((scale*i), (scale*j)+1), ((scale*i), (scale*j)+scale-1))
                if not value and direction == "right":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+scale, (scale*j)+1), ((scale*i)+scale, (scale*j)+scale-1))

    for node in a_star.path:
        print("hello")
        print(str(node.cell) + "cell")
        print(str(maze.start) + "start")

        if node.cell != maze.start:
            print(node.cell.x, node.cell.y, node.previous_cell.x, node.previous_cell.y)
            pygame.draw.line(screen, (0,255,255), (node.cell.x, node.cell.y),(node.previous_cell.x, node.previous_cell.y))


    # Flip the display
    pygame.display.flip()

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Done! Time to quit.
    pygame.quit()

main()