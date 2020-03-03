import math

class Searches:

    def __init__(self, maze):

        self.maze = maze
        self.start = self.maze.start
        self.end = self.maze.end

        self.paths = {}
        self.colours = {
                        "bfs closed": (25,200,25),
                        "bfs path": (255,0,255),
                        "astar closed": (255,0,0),
                        "astar path": (0,0,204)
        }
        self.bfs_algorithm()
        self.a_star_algorithm()

    def bfs_algorithm(self):
        bfs_closed = []
        bfs_path = []

        bfs_frontier = [self.start]

        while len(bfs_frontier) > 0:
            current = bfs_frontier[0]
            bfs_closed.append(bfs_frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    bfs_path.append(current)
                    current = current.bfs_previous
                self.paths["bfs closed"] = bfs_closed
                self.paths["bfs path"] = bfs_path
                return

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell == None:
                        continue
                    if cell in bfs_closed or cell in bfs_frontier:
                        continue
                    cell.set_bfs_previous(current)
                    bfs_frontier.append(cell)

    def a_star_algorithm(self):
        astar_closed = []
        astar_path = []

        frontier = [self.start]

        while len(frontier) > 0:
            frontier.sort(key=lambda x: x.total_distance)
            current = frontier[0]

            astar_closed.append(frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    astar_path.append(current)
                    current = current.astar_previous

                self.paths["astar closed"] = astar_closed
                self.paths["astar path"] = astar_path
                return

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]

                    if cell is None:
                        continue
                    if cell in astar_closed or cell in frontier:
                        continue
                    cell.set_astar_previous(current)
                    distance_to_goal = math.sqrt((cell.x - self.end.x)**2 + (cell.y - self.end.y)**2)
                    cell.update_distance(distance_to_goal)
                    frontier.append(cell)