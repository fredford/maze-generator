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
            return "("+str(self.x)+","+str(self.y)+")"
            #return " 1"
        else:
            return "("+str(self.x)+","+str(self.y)+")"
            #return " 0"