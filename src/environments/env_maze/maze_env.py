
from copy import deepcopy

class MazeEnv():

    # TODO Comments

    def __init__(self, maze):
        self.rows = maze.height
        self.cols = maze.width
        self.start_cell = maze.start
        self.start = [maze.start.x, maze.start.y]
        self.end_cell = maze.end
        self.end = [maze.end.x, maze.end.y]
        self.current_state = None
        self.maze = maze

    def env_start(self):
        """Method called when the episode starts, initializes current state of the environment
        
        Returns:
            state {int} -- The numerical state in the state space
        """

        self.current_state = self.start

        return self.observation(self.current_state)


    def env_step(self, action):
        new_state = deepcopy(self.current_state)
        
        current_cell = self.maze.maze[self.current_state[0]][self.current_state[1]]

        if action == 0:     # right
            move = "right"    
        elif action == 1:   # down
            move = "below"
        elif action == 2:   # left 
            move = "left"
        elif action == 3:   # up
            move = "above"

        if not current_cell.walls[move]:
            new_cell = current_cell.neighbors[move]

        else:
            new_cell = current_cell

        self.current_state = [new_cell.x, new_cell.y]

        # Each time step provides -1 reward for each move
        reward = -1.0
        isTerminal = False
        if new_cell == self.end_cell:
            isTerminal = True
        
        return reward, self.observation(self.current_state), isTerminal



    def observation(self, state):
        """Method takes an [x,y] coordinate state and gets the single value state number
        
        Arguments:
            state {array} -- Array where the x-coordinate is in state[0] and y-coordinate is in state[1]
        
        Returns:
            state {int} -- The state number in the state space
        """
        return state[0] * self.cols + state[1]