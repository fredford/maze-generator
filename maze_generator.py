from random import shuffle, randrange
import numpy as np
import random

class Maze:
    def __init__(self, width, height):

        self.directions = {"above":(0, -1), "below":(0, 1), "left":(-1, 0), "right":(1,0)}
        self.width = width
        self.height = height
        self.maze = []
        self.create_cells()
        self.mesh_cells()
        self.dfs_make_maze()

    def create_cells(self):
        for i in range(self.width):
            temp = []
            for j in range(self.height):
                temp.append(Cell(i, j))
            self.maze.append(temp)

    def mesh_cells(self):
        for row in self.maze:
            for cell in row:
                for direction, (x,y) in self.directions.items():
                    if cell.x + x < 0 or cell.y + y < 0:
                        cell.neighbors[direction] = None
                    elif cell.x + x == self.width or cell.y + y == self.height:
                        cell.neighbors[direction] = None
                    else:
                        cell.neighbors[direction] = self.maze[cell.x + x][cell.y + y]

    def valid_neighbors(self, cell):
        neighbors = []

        for direction in self.directions.keys():
            if cell.neighbors[direction] != None and cell.neighbors[direction].all_walls():
                neighbors.append(cell.neighbors[direction])

        return neighbors

    def dfs_make_maze(self):
        current_cell = self.maze[0][0]
        frontier = self.valid_neighbors(current_cell)
        counter = 0

        while len(frontier) > 0:
            neighbors = self.valid_neighbors(current_cell)
            counter += 1

            if not neighbors:
                current_cell = frontier.pop()
                continue

            next_cell = random.choice(neighbors)
            current_cell.set_path(next_cell)
            next_cell.set_path(current_cell)
            frontier.append(current_cell)
            current_cell = next_cell

    def print_maze(self):
        for i in range(len(self.maze)):
            line = ""
            for j in range(len(self.maze[i])):
                line += str(self.maze[i][j])
            print(line)

class Cell:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.above = None
        self.below = None
        self.left = None
        self.right = None
        self.walls = {"above": True, "below": True, "left": True, "right": True}
        self.neighbors = {}
        self.test = False

    def all_walls(self):
        return all(self.walls.values())

    def set_path(self, cell):
        for direction, neighbor in self.neighbors.items():
            if neighbor != None:
                if cell.x == neighbor.x and cell.y == neighbor.y:
                    self.walls[direction] = False

    def __repr__(self):
        return str(self)

    def __str__(self):

        if all(self.walls.values()):
            return "("+str(self.x)+","+str(self.y)+","+str(sum(self.walls.values()))+")"
            #return " 1"
        else:
            return "("+str(self.x)+","+str(self.y)+","+str(sum(self.walls.values()))+")"
            #return " 0"

