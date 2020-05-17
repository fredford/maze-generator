import math
import sys

class Searcher:
    """Object used to perform and store search related information
    """

    def __init__(self):

        self.maze = None
        self.directions = {"above":(0, -1), "below":(0, 1), "left":(-1, 0), "right":(1,0)}
        self.lengths = {}   # Dictionary of the lengths for each search algorithm
        self.visits = {}    # Dictionary of cells visited for each search algorithm
        self.paths = {}     # Dictionary of path traveled from the start of the search to the end

    def get_grid(self, start, end):
        """Method to get the grid start and end cells.

        Arguments:
            start {Cell} -- Cell object that contains the starting point for the maze
            end {[type]} -- Cell object that contains the ending point for the maze
        """
        self.start = start
        self.end   = end


    def run_BFS(self):
        """Method to perform a Breadth-First Search on given maze. The algorithm works by adding valid neighoring cells to the frontier of the current cell, then going through each cell in the frontier based upon the order in which they are added to the frontier.
        """
        algorithm = "BFS"

        closed = []
        path = []
        frontier = [self.start]

        while len(frontier) > 0:
            current = frontier[0]
            closed.append(frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    path.append(current)
                    current = current.get_previous(algorithm)
                self.visits[algorithm] = closed
                self.paths[algorithm] = path
                self.lengths[algorithm] = len(path)
                return

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell == None:
                        continue
                    if cell in closed or cell in frontier:
                        continue
                    cell.set_previous(algorithm, current)
                    frontier.append(cell)

    def run_Astar(self):
        """Method to perform an A* search on a given maze. The algorithm works by adding valid neighoring cells to the frontier of the current cell, then selecting the cell in the frontier with the lowest total estimated distance to from the start goal to the end goal. The distance from the current cell to the end state is performed using the euclidean distance between the current cell and the end cell.
        """

        algorithm = "A*"

        closed = []
        path = []

        frontier = [self.start]

        while len(frontier) > 0:
            frontier.sort(key=lambda x: x.total_distance)
            current = frontier[0]

            closed.append(frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    path.append(current)
                    current = current.get_previous(algorithm)

                self.visits[algorithm] = closed
                self.paths[algorithm] = path
                self.lengths[algorithm] = len(path)
                return

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]

                    if cell is None:
                        continue
                    if cell in closed or cell in frontier:
                        continue
                    cell.set_previous(algorithm, current)
                    distance_to_goal = math.sqrt((cell.x - self.end.x)**2 + (cell.y - self.end.y)**2)
                    cell.update_distance(distance_to_goal)
                    frontier.append(cell)

    def run_DFS(self):
        """Method to perform a Depth-First Search on a given maze. The algorithm works by adding valid neighoring cells to the frontier of the current cell, then selecting the latest added cell to the frontier and continuing until all cells have been visited.
        """
        algorithm = "DFS"

        closed = []
        path = []
        frontier = [self.start]

        while len(frontier) > 0:
            current = frontier.pop()
            closed.append(current)

            if current == self.end:
                while current != self.start:
                    path.append(current)
                    current = current.get_previous(algorithm)
                self.visits[algorithm] = closed
                self.paths[algorithm] = path
                self.lengths[algorithm] = len(path)

                return

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell == None:
                        continue
                    if cell in closed or cell in frontier:
                        continue
                    cell.set_previous(algorithm, current)
                    frontier.append(cell)
