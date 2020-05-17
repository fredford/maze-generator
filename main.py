import pygame as pg
import sys

from src.button import Button
from src.cell import Cell
from src.utils import Utils

def main():

    window_width = 800
    window_height = 925
    button_height = 25

    pg.init()

    pg.display.set_caption("Maze")
    screen = pg.display.set_mode((window_width, window_height))
    utility = Utils(window_height, window_width, button_height, screen)
    
    utility.create_buttons()
    utility.draw_window()
    
    closed = False
    event_key = None

    # Continue running until the user closes the window
    while not closed:
        utility.handle_event(event_key)
        event_key = None
        utility.draw_window()
        event = pg.event.poll()
        if event.type == pg.QUIT:
            closed = True
        
        elif event.type == pg.MOUSEBUTTONUP:
            for key, button in utility.buttons.items():
                if button.select(event.pos):
                    button.pressed += 1
                    event_key = key

    pg.quit()

main()