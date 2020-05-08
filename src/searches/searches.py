import math

class Searches:

    def __init__(self, maze):
        self.maze = maze
        self.start = self.maze.start
        self.end = self.maze.end
        self.lengths = {}
        self.visits = {}
        self.paths = {}
        self.colours = {
                        "bfs closed": (25,200,25),
                        "bfs": (255,0,255),
                        "astar closed": (255,0,0),
                        "astar": (0,0,204)
        }



    def run_searches(self):

        self.bfs_algorithm()
        self.a_star_algorithm()

        return self.lengths, self.visits, self.paths, self.colours

    def bfs_algorithm(self):

        algorithm = "bfs"

        closed = []
        path = []

        frontier = [self.start]

        while len(frontier) > 0:
            current = frontier[0]
            closed.append(frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    path.append(current)
                    current = current.bfs_previous
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
                    cell.set_bfs_previous(current)
                    frontier.append(cell)

    def a_star_algorithm(self):

        algorithm = "astar"

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
                    current = current.astar_previous

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
                    cell.set_astar_previous(current)
                    distance_to_goal = math.sqrt((cell.x - self.end.x)**2 + (cell.y - self.end.y)**2)
                    cell.update_distance(distance_to_goal)
                    frontier.append(cell)