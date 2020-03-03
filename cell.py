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
        self.previous = None

    def set_previous(self, previous):
        self.previous = previous

    def update_distance(self):
        if self.previous == None:
            self.distance = 0
        else:
            self.distance = self.previous.distance + 1

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