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
        self.distance = 0
        self.total_distance = 0
        self.euclidean_distance = 0
        self.astar_previous = None
        self.bfs_previous = None
        self.q_previous = None

    def set_q_previous(self, q_previous):
        self.q_previous = q_previous

    def set_astar_previous(self, astar_previous):
        self.astar_previous = astar_previous

    def set_bfs_previous(self, bfs_previous):
        self.bfs_previous = bfs_previous

    def set_distance(self, distance):
        self.distance = distance

    def update_distance(self, distance_to_goal):
        if self.astar_previous == None:
            self.distance = 0
            self.total_distance = distance_to_goal
        else:
            self.distance = self.astar_previous.distance + 1
            self.total_distance = self.distance + distance_to_goal

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
            return "("+str(self.x)+","+str(self.y)+","+str(self.distance)+")"
            #return " 1"
        else:
            return "("+str(self.x)+","+str(self.y)+","+str(self.distance)+")"
            #return " 0"