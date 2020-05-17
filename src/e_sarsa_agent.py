import numpy as np

class ExpectedSarsaAgent():

    def agent_init(self, agent_info):
        """Object instance of a Expected Sarsa agent that calculates the expected value of the next state from the potential next actions
        
        num_actions {int} -- The number of actions the agent can take in the environment
        num_states {int} -- The number of states the agent can be in throughout the environment
        epsilon {float} -- The rate at which the agent will choose to explore
        step_size {float} -- The rate at which the agent will learn from each step
        discount {float} -- The amount that a reward is discounted valuing immediate, future or intermediate rewards
        rand_seed {int} -- The number of random values generated
        """

        # Set the agents parameters
        self.num_actions = agent_info["num_actions"]
        self.num_states = agent_info["num_states"]
        self.epsilon = agent_info["epsilon"]
        self.step_size = agent_info["step_size"]
        self.discount = agent_info["discount"]
        self.rand_generator = np.random.RandomState(agent_info["seed"])

        # Initialize the action-value estimates to zero
        self.q = np.zeros((self.num_states, self.num_actions))

    def agent_start(self, state):
        """Method called at the start of each episode to select the first action given a starting state.
        
        Arguments:
            state {int} -- The initial start state in the environment.
        
        Returns:
            action {int} -- The initial action taken by the agent.
        """
        # Select the list of action-value estimates for the current state
        current_q = self.q[state,:]
        # Select the action that the agent will take in the current state
        action = self.action_selection(state, current_q)

        self.prev_state = state
        self.prev_action = action

        return action

    def agent_step(self, reward, state):
        """Method called at each step to evaluate whether the agent will take an exploration action or a greedy action in the state-space. Then update action-value estimates for the previous state and previous action given the expected value of the action value estimate of the current state and action.
        
        Arguments:
            reward {float} -- The reward received for the last action taken from self.prev_action, self.prev_state
            state {int} -- The state in the environment that the agent ended up in after taking the last step.
        
        Returns:
            action {int} -- The action that the agent decided to take.
        """
        # Select the list of action-value estimates for the current state
        current_q = self.q[state,:]
        # Select the action that the agent will take in the current state
        action = self.action_selection(state, current_q)

        # Previous action-value estimate
        prev_q = self.q[self.prev_state, self.prev_action]

        # Summation for greedy action-value selection
        greedy_q = np.max(current_q)
        greedy_sum = (1-self.epsilon)*greedy_q

        # Summation for exploratory action-value selection
        explor_sum = 0
        for action_p in range(self.num_actions):
            explor_sum += (self.epsilon/self.num_actions)*current_q[action_p]

        # Compute and update the action-value estimate for the previous state-action pair
        self.q[self.prev_state, self.prev_action] = prev_q + self.step_size * (reward + self.discount *(explor_sum + greedy_sum) - prev_q)

        # Set the current state-action pair to be the previous state-action pair
        self.prev_state = state
        self.prev_action = action

        return action

    def agent_end(self, reward):
        """Method called in the terminal state where the final action-value estimate update is performed given the previous state and action.
        
        Arguments:
            reward {float} -- The reward the agent received for entering the terminal state.
        """
        prev_q = self.q[self.prev_state, self.prev_action]
        self.q[self.prev_state, self.prev_action] = prev_q + self.step_size*(reward - prev_q)

    def argmax(self, q_values):
        """argmax with random tie-breaking
        Args:
            q_values (Numpy array): the array of action-values
        Returns:
            action (int): an action with the highest value
        """
        top = float("-inf")
        ties = []

        for i in range(len(q_values)):
            if q_values[i] > top:
                top = q_values[i]
                ties = []

            if q_values[i] == top:
                ties.append(i)

        return self.rand_generator.choice(ties)

    def action_selection(self, state, current_q):
        """Method called in choosing whether to explore or take the action which would provide a greedy action-value estimate
        
        Arguments:
            state {int} -- The current state that the agent is in
        
        Returns:
            action {int} -- The action that the agent will take in the current state
        """
        # Randomly generate a number between 0 and 1
        # If the number is less than epsilon, explore
        if self.rand_generator.rand() < self.epsilon:
            return self.rand_generator.randint(self.num_actions)

        # If the number is greater than epsilon, choose the greedy option
        else:
            return self.argmax(current_q)