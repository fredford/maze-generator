class A_star:

    def __init__(self, maze):

        self.maze = maze
        self.start = self.maze.start
        self.end = self.maze.end
        self.path = []
        self.nodes = []
        self.final_path = ""

        self.a_star_algorithm()

    def a_star_algorithm(self):
        frontier = [self.start]
        self.closed = []
        count = 0

        while len(frontier) > 0 and count < 10000:

            print("Frontier")
            print(frontier)

            frontier.sort(key=lambda x: x.distance)
            current = frontier[0]
            print("Current")
            print(current)

            if current == self.end:
                while current != self.start:
                    self.path.append(current)
                    current = current.previous

            self.closed.append(frontier.pop(0))

            print("Frontier pop")
            print(frontier)

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell in self.closed or cell in frontier:
                        continue
                    cell.set_previous(current)
                    cell.update_distance()
                    frontier.append(cell)


            count += 1


class Node:

    def __init__(self, current_cell, last_cell=None, previous_node=None):
        self.cell = current_cell
        self.previous_cell = last_cell
        self.previous_node = previous_node
        self.distance = 0
        self.path_to_start = ""
        self.update_distance()
        self.update_path()

    def update_distance(self):
        if self.previous_cell == None:
            self.distance = 0
        else:
            self.distance = self.previous_node.distance + 1

    def update_path(self):
        if self.previous_cell == None:
            self.path_to_start = str(self.cell)
        else:
            self.path_to_start = self.previous_node.path_to_start + str(self.cell)

    def __repr__(self):
        return str(self)

    def __str__(self):
        #return self.path_to_start+","+str(self.distance)
        return str(self.cell)