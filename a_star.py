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
        node = self.add_node(self.start, None, None)
        frontier = [node]
        count = 0

        while len(frontier) > 0 and count < 20:
            node = self.minimal_path(frontier)

            frontier.remove(node)
            self.path.append(node)
            if node.cell == self.end:
                return node.path_to_start

            print(node.cell.neighbors)
            for neighbor in node.cell.neighbors.values():
                frontier.append(self.add_node(neighbor, node.cell, node))

            count += 1


    def add_node(self, current_cell, last_cell, last_node):
        node = Node(current_cell, last_cell, last_node)
        self.nodes.append(node)
        return node


    def minimal_path(self, frontier):
        min_path = min(frontier, key=lambda x: x.distance)
        #print(min_path)
        return min_path


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
        return self.path_to_start+","+str(self.distance)