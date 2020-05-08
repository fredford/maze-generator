
from copy import deepcopy

class CliffWorldEnv():
    """Implementation of the Cliffworld environment commonly used in Reinforcement Learning to test Q-Learning, Sarsa and Expected Sarsa
    """

    def __init__(self):
        self.rows = 4
        self.cols = 12
        self.start = [0,0]
        self.goal = [0,11]
        self.current_state = None

    def env_start(self):
        """Method called when the episode starts, initializes current state of the environment
        
        Returns:
            state {int} -- The numerical state in the state space
        """

        self.current_state = self.start

        return self.observation(self.current_state)


    def env_step(self, action):
        new_state = deepcopy(self.current_state)

        if action == 0: #right
            new_state[1] = min(new_state[1]+1, self.cols-1)
        elif action == 1: #down
            new_state[0] = max(new_state[0]-1, 0)
        elif action == 2: #left
            new_state[1] = max(new_state[1]-1, 0)
        elif action == 3: #up
            new_state[0] = min(new_state[0]+1, self.rows-1)
        else:
            raise Exception("Invalid action.")
        self.current_state = new_state

        # Each time step provides -1 reward for each move
        reward = -1.0
        isTerminal = False
        if self.current_state[0] == 0 and self.current_state[1] > 0:
            if self.current_state[1] < self.cols - 1:
                reward = -100.0
                self.current_state = deepcopy(self.start)
            else:
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