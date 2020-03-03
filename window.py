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

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.screen.fill([255,255,255])

        #Buttons
        


    #def start_menu(self):
        

    def create_buttons(self):
        #height_minus = 90
        #size_size = 20
        #size_minus = pygame.Rect((self.window_width-90, height_minus, size_size, size_size))
        #size_minus_border = pygame.Rect((self.window_width-88, height_minus, size_size-2, size_size-2))
        #size_plus = pygame.Rect((self.window_width-20, height_minus, size_size, size_size))
        menu = pygame.Rect((self.window_width/4, self.window_height/4, self.window_width/2, self.window_height/2))

        self.buttons = [menu]

    def draw(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, [0, 0, 0], button)

        pygame.display.flip()


    def run_window(self):
        while not self.close_clicked:
            #self.create_buttons()
            self.draw()
            self.handle_event()
            #self.draw()
            #if self.continue_window:
            #    self.update()
            #    self.decide_continue()
            time.sleep(self.pause_time)

        pygame.quit()

    def handle_event(self):
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        elif event.type == MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up_event(event)

        


window = Window()
window.run_window()