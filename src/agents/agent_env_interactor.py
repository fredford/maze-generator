
class Interactor():

    def __init__(self, env_object, agent_class, agent_info):
        self.environment = env_object
        self.agent = agent_class()
        self.agent.agent_init(agent_info)
        
        self.total_reward = 0.0
        self.num_steps = 0
        self.num_episodes = 0

        self.last_action = None

    def start(self):        

        self.total_reward = 0.0
        self.num_steps = 1

        last_state = self.environment.env_start()
        self.last_action = self.agent.agent_start(last_state)

        return last_state, self.last_action
    

    def step(self):

        reward, last_state, isTerminal = self.environment.env_step(self.last_action)

        self.total_reward += reward;

        if isTerminal:
            self.num_episodes += 1
            self.agent.agent_end(reward)

            return reward, last_state, None, isTerminal

        else:
            self.num_steps += 1
            self.last_action = self.agent.agent_step(reward, last_state)

            return reward, last_state, self.last_action, isTerminal

    def episode(self, max_steps):

        isTerminal = False

        self.start()

        while (not isTerminal) and ((max_steps == 0) or (self.num_steps < max_steps)):
            step_result = self.step()
            isTerminal = step_result[3]

        return isTerminal

    def get_total_reward(self):
        return self.total_reward

    def get_num_steps(self):
        return self.num_steps

    def get_num_episodes(self):
        return self.num_episodes