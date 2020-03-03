import random
import cell

class Maze:
    def __init__(self, width, height):
        self.directions = {"above":(0, -1), "below":(0, 1), "left":(-1, 0), "right":(1,0)}
        self.width = width
        self.height = height
        self.start = None
        self.end = None
        self.maze = []
        self.create_cells()
        self.mesh_cells()
        self.dfs_make_maze()
        self.set_start_end()

    def create_cells(self):
        for i in range(self.width):
            temp = []
            for j in range(self.height):
                temp.append(cell.Cell(i, j))
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

    def set_start_end(self):
        start = (random.randint(0, self.width), random.randint(0, self.height))
        end = start
        while start == end:
            end = (random.randint(0, self.width), random.randint(0, self.height))
        print(start)
        print(end)
        print(len(self.maze))
        print(len(self.maze[0]))

        self.start = self.maze[start[0]][start[1]]
        self.end = self.maze[end[0]][end[1]]

    def print_maze(self):
        for i in range(len(self.maze)):
            line = ""
            for j in range(len(self.maze[i])):
                line += str(self.maze[i][j])
            print(line)

