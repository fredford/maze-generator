import random
from src import cell

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Maze:
    """Object used to represent a maze and the information needed to specify the dimensions, cells contained, start and finish.
    """
    def __init__(self, size, scale):
        self.directions = {"above":(0, -1), "below":(0, 1), "left":(-1, 0), "right":(1,0)}
        
        self.size = size
        self.scale = scale

        self.start = None
        self.end = None
        self.grid = []
        self.create_cells()
        self.mesh_cells()
        self.set_start_end()

    def create_cells(self):
        """Method to create the required number of cells for the maze.
        """
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(cell.Cell(i, j, self.scale))
            self.grid.append(temp)

    def mesh_cells(self):
        """Method to mesh the cells of the grid together so they are connected for usage and manipulation.
        """
        for row in self.grid:
            for cell in row:
                for direction, (x,y) in self.directions.items():
                    if cell.x + x < 0 or cell.y + y < 0:
                        cell.neighbors[direction] = None
                    elif cell.x + x == self.size or cell.y + y == self.size:
                        cell.neighbors[direction] = None
                    else:
                        cell.neighbors[direction] = self.grid[cell.x + x][cell.y + y]

    def set_start_end(self):
        """Method to set the start and end of the maze, by randomly picking two locations and setting the corresponding information in cells chosen.
        """
        start = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        end = start
        while start == end:
            end = (random.randint(0, self.size-1), random.randint(0, self.size-1))

        self.start = self.grid[start[0]][start[1]]
        self.end = self.grid[end[0]][end[1]]

        self.start.isStart = True
        self.end.isEnd = True

        self.start.background = BLUE
        self.end.background = RED

    def update_start_end(self):
        """Method to update the start and end of the maze.
        """
        for row in self.grid:
            for cell in row:
                if cell.isStart:
                    self.start = cell
                elif cell.isEnd:
                    self.end = cell

    def change_start(self, new_start):
        """Method to change the location of the start of the maze and remove the previous start location information.

        Arguments:
            new_start {Cell} -- The new starting location for the maze.
        """
        self.start.isStart = False
        self.start.background = WHITE
        self.start = new_start
        self.start.isStart = True
        self.start.background = BLUE

    def change_end(self, new_end):
        """Method to change the location of the end of the maze and remove the previous end location information.

        Arguments:
            new_end {Cell} -- The new ending location for the maze.
        """
        self.end.isEnd = False
        self.end.background = WHITE
        self.end = new_end
        self.end.isEnd = True
        self.end.background = RED

