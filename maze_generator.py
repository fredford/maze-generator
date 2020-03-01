from random import shuffle, randrange
import numpy as np
import random

class Maze:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.maze = []
        self.create_cells()
        self.set_border()
        self.mesh_cells()
        self.dfs_make_maze()

    def dfs_make_maze(self):

        frontier = []

        frontier.append(self.maze[1][1])

        counter = 0

        while len(frontier) > 0 and counter < 20:
            self.print_maze()

            random.shuffle(frontier)
            #print(frontier)

            if counter == 0:
                current_cell = frontier.pop()
                current_cell.set_path()

            neighbors = self.valid_neighbors(current_cell)


            if not neighbors:
                current_cell = frontier.pop()
                continue

            next_cell = random.choice(neighbors)
            next_cell.set_path()
            frontier.append(current_cell)
            current_cell = next_cell

            counter += 1
            print(counter)

        self.print_maze()


    def valid_neighbors(self, cell):
        neighbors = []
        if not cell.above.isBorder and cell.above.all_Walls():
            neighbors.append(cell.above)
        if not cell.below.isBorder and cell.below.all_Walls():
            neighbors.append(cell.below)
        if not cell.right.isBorder and cell.right.all_Walls():
            neighbors.append(cell.right)
        if not cell.left.isBorder and cell.left.all_Walls():
            neighbors.append(cell.left)

        return neighbors


    def create_cells(self):
        for i in range(self.width):
            temp = []
            for j in range(self.height):
                temp.append(Cell(i, j))

            self.maze.append(temp)

    def set_border(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i == 0 or j == 0 or i == len(self.maze)-1 or j == len(self.maze[i])-1:
                    cell = self.maze[i][j]
                    cell.set_border()

    def mesh_cells(self):
        for i in range(1,len(self.maze)-1):
            for j in range(1,len(self.maze[i])-1):
                cell = self.maze[i][j]
                cell.set_cells(self.maze[i-1][j], self.maze[i+1][j], self.maze[i][j-1], self.maze[i][j+1])

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
        self.isFilled = True
        self.isStart = False
        self.isEnd = False
        self.isBorder = False

    def set_cells(self, above, below, left, right):

        self.above = above
        self.below = below
        self.left = left
        self.right = right

    def set_start(self):
        self.isStart = True

    def set_end(self):
        self.isEnd = True

    def set_path(self):
        self.isFilled = False

    def set_border(self):
        self.isBorder = True
        self.isFilled = False

    def all_Walls(self):
        self.get_neighbors()
        return all(self.neighbors)

    def get_neighbors(self):
        neighbors = []

        if not self.above.isBorder:
            neighbors.append(self.above)
        if not self.below.isBorder:
            neighbors.append(self.below)
        if not self.left.isBorder:
            neighbors.append(self.left)
        if not self.right.isBorder:
            neighbors.append(self.right)

        self.neighbors = neighbors

    def __str__(self):
        if self.isFilled:
            return " 1"
        if self.isBorder:
            return " 4"
        if self.isStart:
            return " S"
        if self.isEnd:
            return " E"
        else:
            return " 0"