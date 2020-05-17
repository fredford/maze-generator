import random
import copy
import sys

sys.setrecursionlimit(30000)

class Generator:
    """ Object representing a Generator used to generate the maze specified by the user.
    """

    def __init__(self):

        self.maze = None
        self.directions = {"above":(0, -1), "below":(0, 1), "left":(-1, 0), "right":(1,0)}
        self.recursive_list = []

    def run_generator(self, event_key):
        """Method used to run the generation algorithm specified by the user.

        Arguments:
            event_key {string} -- String representing the button the user pressed

        Raises:
            Exception: The instance where an event key is not passed or is invalid.

        """
        if event_key == "genDFS":
            return self.make_DFS()
        elif event_key == "Prims":
            return self.make_Prims()
        elif event_key == "Recursive":
            return self.make_Recursive()
        else:
            raise Exception ("Missing event key")

    def get_grid(self, grid):
        """Method used to update the grid of the generator. Set a temporary maze that circumvents the visualized generation process. Set the starting cell to begin generating the maze from.

        Arguments:
            grid {list} -- list of lists representing the cells in the grid.
        """
        self.maze = grid
        self.temp_maze = copy.deepcopy(self.maze)
        self.start = (random.randint(0, len(self.maze)-1), random.randint(0, len(self.maze)-1))

    def valid_neighbors(self, cell):
        """Method used to generate a list of valid neighboring cells to visit.

        Arguments:
            cell {Cell} -- A Cell object representing the location on the grid and the data stored in that location.

        Returns:
            neighbors -- A list of Cell objects neighboring the specified cell.
        """
        neighbors = []

        for direction in self.directions.keys():
            if cell.neighbors[direction] != None and cell.neighbors[direction].all_walls():
                neighbors.append(cell.neighbors[direction])

        return neighbors

    def make_DFS(self):
        """Method used to generate a maze according to the Depth First Search algorithm. This works by continuously checking the neighboring cells of a cell until all neighboring cells have been visited.

        Returns:
            maze_list -- A list of tuple Cell objects representing the locations where a path was established between two cells.
        """
        maze_list = []

        sys.setrecursionlimit(30000)
        
        current_cell = self.temp_maze[self.start[0]][self.start[1]]
        maze_list.append((current_cell, current_cell))
        frontier = self.valid_neighbors(current_cell)

        while len(frontier) > 0:
            neighbors = self.valid_neighbors(current_cell)

            if not neighbors:
                current_cell = frontier.pop()
                continue

            next_cell = random.choice(neighbors)
            maze_list.append((current_cell, next_cell))
            
            frontier.append(current_cell)
            current_cell.set_path(next_cell)
            next_cell.set_path(current_cell)
            current_cell = next_cell

        return maze_list

    def make_Prims(self):
        """Method used to generate a maze according to Prim's algorithm. This works by randomly selecting a cell from the frontier and adding all additional valid neighbors to the frontier each time. This is repeated until all cells have been visited.

        Returns:
            maze_list -- A list of tuple Cell objects representing the locations where a path was established between two cells.
        """
        sys.setrecursionlimit(30000)
        maze_list = []
        
        current_cell = self.temp_maze[self.start[0]][self.start[1]]
        maze_list.append((current_cell, current_cell))
        
        neighbors = self.valid_neighbors(current_cell)

        visited = [current_cell]

        frontier = []

        for neighbor in neighbors:
            frontier.append([neighbor, current_cell])

        counter = 0

        while len(frontier) > 0:
            neighbors = self.valid_neighbors(current_cell)

            for neighbor in neighbors:
                if [neighbor, current_cell] not in frontier and neighbor not in visited:
                    frontier.append([neighbor, current_cell])

            for next_cell, current_cell in frontier:
                if next_cell in visited:
                    frontier.remove([next_cell, current_cell])
           
            if len(frontier) == 0:
                break

            next_cell, current_cell = random.choice(frontier)
            frontier.remove([next_cell, current_cell])
            maze_list.append((current_cell, next_cell))

            if next_cell not in visited:
                visited.append(next_cell)
                current_cell.set_path(next_cell)
                next_cell.set_path(current_cell)
                current_cell = next_cell
            counter += 1

        return maze_list

    def make_Recursive(self):
        """Method used to generate a maze according to the Recursive Division algorithm. Where 4 chambers are established, then 3 walls are selected to be opened from the 4 newly established chambers. This process is repeated recursively until the base cases have been reached, where either the chamber cannot be broken into 4 sections therefore the middle wall is removed, or the overall size is too small to be subdivided at all.

        Returns:
            recursive_list -- A list of tuple Cell objects representing the locations where a path was established between two cells.
        """
        sys.setrecursionlimit(30000)

        self.recursive_function()
        
        output = self.recursive_list
        self.recursive_list = []

        return output

    def recursive_function(self, chamber=None):
        """Method recursively called to generate a maze according to the Recursive Division algorithm.

        Keyword Arguments:
            chamber {tuple} -- A tuple of integer values representing the dimensions of the chambers (default: {None})
        """
        # Starting the method with no provided chambers, the initial grid dimensions are set.
        if chamber is None:
            chamber_left = 0
            chamber_top = 0
            chamber_width = len(self.temp_maze)
            chamber_height = len(self.temp_maze[0])
        # Use the recursively provided chamber values to set the dimensions of the current chamber.
        else:
            chamber_left = chamber[0]
            chamber_top = chamber[1]
            chamber_width = chamber[2]
            chamber_height = chamber[3]

        # Set the dividing points in the current chamber.
        x_divide = int(chamber_width/2)
        y_divide = int(chamber_height/2)

        # If the current chamber is wide enough to create a wall, then a wall is created between the two cells horizontally.
        if chamber_width > 1:
            for y in range(chamber_height):
                self.temp_maze[chamber_left + x_divide][chamber_top + y].walls["left"] = True
                self.temp_maze[chamber_left + x_divide-1][chamber_top + y].walls["right"] = True
                self.recursive_list.append((self.temp_maze[chamber_left + x_divide][chamber_top + y], self.temp_maze[chamber_left + x_divide-1][chamber_top + y], "wall"))
                
        # If the current chamber is tall enough to create a wall, then a wall is created between the two cells vertically.
        if chamber_height > 1:
            for x in range(chamber_width):
                self.temp_maze[chamber_left + x][chamber_top + y_divide].walls["above"] = True
                self.temp_maze[chamber_left + x][chamber_top + y_divide - 1].walls["below"] = True
                self.recursive_list.append((self.temp_maze[chamber_left + x][chamber_top + y_divide], self.temp_maze[chamber_left + x][chamber_top + y_divide - 1],"wall"))

        # If the current chamber is not tall enough to create a wall or wide enough to create a wall, then return.
        if chamber_width < 2 and chamber_height < 2:
            return

        # Set the dimensions of the next chambers
        top_left  = (chamber_left            , chamber_top            , x_divide                 , y_divide)
        top_right = (chamber_left + x_divide , chamber_top            , chamber_width - x_divide , y_divide)
        bot_left  = (chamber_left            , chamber_top + y_divide , x_divide                 , chamber_height - y_divide)
        bot_right = (chamber_left + x_divide , chamber_top + y_divide , chamber_width - x_divide , chamber_height - y_divide)
 
        chambers = (top_left, top_right, bot_left, bot_right)

        # Set the dimensions of the walls established by this chamber
        left  = ("left"  , chamber_left           , chamber_left + x_divide      , chamber_top + y_divide)
        right = ("right" , chamber_left + x_divide, chamber_left + chamber_width , chamber_top + y_divide)
        top   = ("top"   , chamber_top            , chamber_top  + y_divide      , chamber_left + x_divide - 1) 
        bottom= ("bottom", chamber_top + y_divide , chamber_top  + chamber_height, chamber_left + x_divide - 1)
        
        walls = (left, right, top, bottom)
        
        gaps = 3

        # If the chamber is wide enough to create a wall, but not tall enough to create a wall then break the wall.
        if chamber_width == 2 and chamber_height == 1:
            self.temp_maze[chamber_left][chamber_top].walls["right"] = False
            self.temp_maze[chamber_left+1][chamber_top].walls["left"] = False
            self.recursive_list.append((self.temp_maze[chamber_left][chamber_top], self.temp_maze[chamber_left+1][chamber_top], "clear"))
        # If the chamber is tall enough to create a wall, but not wide enough to create a wall then break the wall.
        elif chamber_width == 1 and chamber_height == 2:
            self.temp_maze[chamber_left][chamber_top].walls["below"] = False
            self.temp_maze[chamber_left][chamber_top+1].walls["above"] = False
            self.recursive_list.append((self.temp_maze[chamber_left][chamber_top], self.temp_maze[chamber_left][chamber_top+1], "clear"))
        # If the chamber is wide enough and tall enough, proceed.
        else:
            # Randomly sample 3 walls established and randomly select a cell on the wall to create a path through.
            for wall in random.sample(walls, gaps):
                if wall[0] == "left" or wall[0] == "right":

                    y = wall[3]

                    if wall[1] == wall[2]:
                        x = wall[1]

                    else:

                        while True:
                            x = random.randrange(wall[1], wall[2])
                            if (self.temp_maze[x][y], self.temp_maze[x][y-1], "clear") not in self.recursive_list:
                                break
                    self.temp_maze[x][y].walls["above"] = False
                    self.temp_maze[x][y-1].walls["below"] = False
                    self.recursive_list.append((self.temp_maze[x][y], self.temp_maze[x][y-1], "clear"))

                else:
                    x = wall[3]

                    if wall[1] == wall[2]:
                        y = wall[1]
                    else:
                        while True:       
                            y = random.randrange(wall[1], wall[2])
                            if (self.temp_maze[x][y], self.temp_maze[x+1][y], "clear") not in self.recursive_list:
                                break
                    self.temp_maze[x][y].walls["right"] = False
                    self.temp_maze[x+1][y].walls["left"] = False
                    self.recursive_list.append((self.temp_maze[x][y], self.temp_maze[x+1][y], "clear"))
        # Recursively go through each chamber set up.
        for num, chamber in enumerate(chambers):
            self.recursive_function(chamber)