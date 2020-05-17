import pygame as pg

class Button():
    """Object used to represent a button used in the GUI
    """

    def __init__(self, color, x, y, width, height, text="", action=None):

        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.text = text
        self.rectangle = pg.Rect((self.x,self.y), (self.width,self.height))
        self.action = action
        self.status = False
        self.pressed = 0

    def draw(self, window, outline=None):
        """Method used to draw the button.

        Arguments:
            window {display} -- The object representing the window to draw on.

        Keyword Arguments:
            outline {COLOR} -- The color of the outline (default: {None})
        """
        
        if outline:
            pg.draw.rect(window, outline, (self.x, self.y, self.width, self.height), 0)

        pg.draw.rect(window, self.color, (self.x+1, self.y+1, self.width-1, self.height-1),0)

        if self.text != '':
            font = pg.font.SysFont('arial', 16)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text,(self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))

    def select(self, mouse_position):
        """Method to determine if the mouse_position collided with the rectangle held by the button.

        Arguments:
            mouse_position {(x,y)} -- Tuple coordinates to be used in comparison with the position held by the button.

        Returns:
            Boolean -- True or False depending on if the mouse position collided with the rectangle held by the button.
        """
        return self.rectangle.collidepoint(mouse_position)