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
        self.clear_history()

        bfs_closed = []
        bfs_path = []

        frontier = [self.start]

        while len(frontier) > 0:
            current = frontier[0]
            bfs_closed.append(frontier.pop(0))

            if current == self.end:
                while current != self.start:
                    bfs_path.append(current)
                    current = current.previous
                continue

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell in bfs_closed or cell in frontier:
                        continue
                    cell.set_previous(current)
                    frontier.append(cell)

        self.paths["bfs closed"] = bfs_closed
        self.paths["bfs path"] = bfs_path

    def a_star_algorithm(self):
        self.clear_history()

        astar_closed = []
        astar_path = []

        frontier = [self.start]

        while len(frontier) > 0:
            frontier.sort(key=lambda x: x.distance)
            current = frontier[0]

            if current == self.end:
                while current != self.start:
                    astar_path.append(current)
                    current = current.previous

                self.paths["astar closed"] = astar_closed
                self.paths["astar path"] = astar_path
                return

            astar_closed.append(frontier.pop(0))

            for direction, wall in current.walls.items():
                if not wall:
                    cell = current.neighbors[direction]
                    if cell in astar_closed or cell in frontier:
                        continue
                    cell.set_previous(current)
                    cell.update_distance()
                    frontier.append(cell)

    def clear_history(self):
        for row in self.maze.maze:
            for cell in row:
                cell.previous = None