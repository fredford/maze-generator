import pygame
import os
from pygame.key import get_pressed, name
from pygame import init, quit, Color, Surface, Rect, KEYUP, K_SPACE, K_RETURN, K_z, K_LSHIFT, K_RSHIFT, K_CAPSLOCK, K_BACKSPACE
from pygame.locals import *
import time

class Window:

    def __init__(self):
        pygame.init()
        self.board_size = 20
        self.window_height = 600
        self.window_width = 600
        self.window_size = self.window_height
        self.pause_time = 0.01
        self.close_clicked = False
        self.continue_game = True
        self.buttons = []

        self.font_size = 32

        # Colours
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 128)
        self.BLACK = (0,0,0)
        self.LGREY = (201,201,201)
        self.DGREY = (176,176,176)

        self.astar_status = False
        self.bfs_status = False
        self.maze_status = False

        self.font = pygame.font.SysFont('arial', self.font_size)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.screen.fill(self.WHITE)

        #Buttons

    def create_menu(self):
        self.screen.fill(self.WHITE)
        self.menu = pygame.Rect((self.window_width/4, self.window_height/4, self.window_width/2, self.window_height/2))
        self.input_border = pygame.Rect((self.window_width*(2/5)-51, (self.window_height*(2/5))-2, 51, 52))
        self.input_box = pygame.Rect((self.window_width*(2/5)-50, self.window_height*(2/5), 50, 50))

        self.astar_toggle = pygame.Rect(((self.window_width/4 + 50), self.window_height*(3/5)+20, 50, 50))
        self.bfs_toggle = pygame.Rect(((self.window_width*(2/4) + 50), self.window_height*(3/5)+20, 50, 50))
        #self.generate_button = pygame.Rect(((self.window_width*(2/4) + 50), self.window_height), 100, 50)

        title = self.font.render(' Maze Solver ', True, self.BLACK, self.WHITE)
        board_size_text = self.font.render('Board Size:', True, self.BLACK, self.WHITE)
        solve_text = self.font.render('Solve:', True, self.BLACK, self.WHITE)
        astar_text = self.font.render('A*', True, self.BLACK, self.WHITE)
        bfs_text = self.font.render('BFS', True, self.BLACK, self.WHITE)
        generate_button = self.font.render('SOLVE', True, self.WHITE, self.BLACK)


        titleRect = title.get_rect()
        boardRect = board_size_text.get_rect()
        solveRect = solve_text.get_rect()
        astarRect = astar_text.get_rect()
        bfsRect = bfs_text.get_rect()
        self.genRect = generate_button.get_rect()
        titleRect.center = (self.window_width // 2, (self.window_height // 4) + (self.font_size/2))
        boardRect.bottomleft = (self.window_width/4 + 5, self.window_height*(2/5)-1)
        solveRect.bottomleft = (self.window_width/4 + 5, self.window_height*(3/5))
        astarRect.bottomleft = (self.window_width/4 + 5, self.window_height*(3.5/5))
        bfsRect.bottomleft = (self.window_width*2/4, self.window_height*(3.5/5))
        self.genRect.topleft = (self.window_width/2 + 30, self.window_height*(2/5))

        pygame.draw.rect(self.screen, self.BLACK, self.menu, 2)
        pygame.draw.rect(self.screen, self.BLACK, self.input_border,2)
        pygame.draw.rect(self.screen, self.LGREY, self.input_box)

        if self.astar_status:
            pygame.draw.rect(self.screen, self.BLACK, self.astar_toggle)
        else:
            pygame.draw.rect(self.screen, self.BLACK, self.astar_toggle, 2)
        if self. bfs_status:
            pygame.draw.rect(self.screen, self.BLACK, self.bfs_toggle)
        else:
            pygame.draw.rect(self.screen, self.BLACK, self.bfs_toggle, 2)

        self.screen.blit(title, titleRect)
        self.screen.blit(board_size_text, boardRect)
        self.screen.blit(solve_text, solveRect)
        self.screen.blit(astar_text, astarRect)
        self.screen.blit(bfs_text, bfsRect)
        self.screen.blit(generate_button, self.genRect)

        pygame.display.flip()

    def run_window(self):
        while not self.close_clicked:
            self.create_menu()
            self.handle_event()
            #self.draw()
            if self.maze_status:
                self.draw()
                self.handle_event()
            #    self.update()
            #    self.decide_continue()
            time.sleep(self.pause_time)

        pygame.quit()

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        elif event.type == MOUSEBUTTONUP and self.continue_game:
            if self.astar_toggle.collidepoint(event.pos):
                self.astar_status = not self.astar_status

            if self.bfs_toggle.collidepoint(event.pos):
                self.bfs_status = not self.bfs_status

            if self.genRect.collidepoint(event.pos):
                self.maze_status = True

    def draw(self):
        self.screen.fill(self.GREEN)
        pygame.display.flip()
        self.maze_status = False
    


window = Window()
window.run_window()