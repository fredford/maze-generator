import maze_generator
import pygame, time
import maze as mg
#from window import Window
import searches


def main():
    pygame.init()
    board_size = 20
    window_size = 600
    scale = window_size/board_size
    clock = pygame.time.Clock()

    pygame.display.set_caption("Maze")
    screen = pygame.display.set_mode((window_size, window_size))
    #myFont = pygame.font.SysFont('arial', 14)

    maze = mg.Maze(board_size, board_size)
    search_results = searches.Searches(maze)


    running = True

    draw_grid(screen, scale, maze, window_size)

    for name in search_results.paths.keys():
        print(name)
        for cell in search_results.paths[name]:
            print(cell, cell.previous)
            if cell != maze.start:
                pygame.draw.line(screen, search_results.colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.previous.x*scale+(scale/2), cell.previous.y*scale+(scale/2)))

            clock.tick(30)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    time.sleep(0.01)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    #for name in search_results.paths.keys():
    #    for cell in search_results.paths[name]:
    #        if cell != maze.start:
    #            pygame.draw.line(screen, search_results.colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.previous.x*scale+(scale/2), cell.previous.y*scale+#(scale/2)))
    #            time.sleep(0.01)
    #            pygame.display.flip()

    # Flip the display
    #pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def draw_grid(screen, scale, maze, window_size):
    cells = maze.maze
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0,0,255), (maze.start.x*scale+(scale/4), maze.start.y*scale+(scale/4), scale/2, scale/2))
    pygame.draw.rect(screen, (255,0,0), (maze.end.x*scale+(scale/4), maze.end.y*scale+(scale/4), scale/2, scale/2))

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

    pygame.display.flip()



def draw(screen, search_results):
    pass

main()