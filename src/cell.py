import pygame as pg

from src.utils import WHITE, BLACK

class Cell:
    """Object representing a single single in the grid, containing all of the information about its positioning, walls, conditions.
    """

    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.above = None
        self.below = None
        self.left = None
        self.right = None
        self.walls = {"above": True, "below": True, "left": True, "right": True}
        self.neighbors = {}
        self.border = WHITE
        self.background = WHITE
        self.isStart = False
        self.isEnd = False
        self.rectangle = pg.Rect((self.x*scale,self.y*scale), (scale,scale))

        self.distance = 0
        self.total_distance = 0
        self.euclidean_distance = 0
        self.astar_previous = None
        self.bfs_previous = None
        self.q_previous = None
        self.dfs_previous = None

    def all_walls(self):
        """Method to return if the cell has all of its walls.

        Returns:
            Boolean -- True or False depending on if the cell has all of its walls
        """
        return all(self.walls.values())

    def set_path(self, cell):
        """Method to set the path between a cell and the neighboring cell.

        Arguments:
            cell {Cell} -- Cell object representing a cell that is a neighbor of the current object.
        """
        for direction, neighbor in self.neighbors.items():
            if neighbor != None:
                if cell.x == neighbor.x and cell.y == neighbor.y:
                    self.walls[direction] = False

    def set_wall(self, cell):
        """Method to set the wall between a cell and the neighboring cell

        Arguments:
            cell {Cell} -- Cell object representing a cell that is a neighbor of the current object.
        """
        for direction, neighbor in self.neighbors.items():
            if neighbor != None:
                if cell.x == neighbor.x and cell.y == neighbor.y:
                    self.walls[direction] = True

    def select(self, mouse_position):
        """Method to determine if the mouse_position collided with the rectangle held by the cell.

        Arguments:
            mouse_position {(x,y)} -- Tuple coordinates to be used in comparison with the position held by the cell.

        Returns:
            Boolean -- True or False depending on if the mouse position collided with the rectangle held by the cell.
        """
        return self.rectangle.collidepoint(mouse_position)

    def changeBackground(self):
        """Change the background of the cell.
        """
        if self.background == WHITE:
            self.background = BLACK
            for direction, wall in self.walls.items():
                if not wall:
                    self.walls[direction] = True

        elif self.background == BLACK:
            self.background = WHITE

    def set_previous(self, search, cell):
        """Method used to set the previous cell to the current cell in the specified search pathway.

        Arguments:
            search {string} -- The search algorithm being performed.
            cell {Cell} -- The Cell object that was previous to the current cell.
        """

        if search == "A*":
            self.astar_previous = cell
        elif search == "BFS":
            self.bfs_previous = cell
        elif search == "QLearning":
            self.q_previous = cell
        elif search == "DFS":
            self.dfs_previous = cell

    def get_previous(self, search):
        """Method used to get the previous cell to the current cell in the specified search exploration.

        Arguments:
            search {string} -- The search algorithm being performed.

        Returns:
            Cell -- The Cell object that was previous to the current cell.
        """

        if search == "A*" or search == "Explore_A*":
            return self.astar_previous
        elif search == "BFS" or search == "Explore_BFS":
            return self.bfs_previous
        elif search == "QLearning":
            return self.q_previous
        elif search == "DFS" or search == "Explore_DFS":
            return self.dfs_previous

    def update_distance(self, distance_to_goal):
        """Method used to update the distance of the current cell to the goal and update the total distance estimated.

        Arguments:
            distance_to_goal {int} -- The integer distance to the goal from the current cell
        """
        if self.astar_previous == None:
            self.distance = 0
            self.total_distance = distance_to_goal
        else:
            self.distance = self.astar_previous.distance + 1
            self.total_distance = self.distance + distance_to_goal

    def __str__(self):
        return str(self.x)+","+str(self.y)

    def __repr__(self):
        return str(self.x)+","+str(self.y)