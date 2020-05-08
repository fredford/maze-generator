import numpy as np

from src.agents.q_learning_agent import QLearningAgent

import unittest

class QLearningAgentTest(unittest.TestCase):
    """
    Unit testing for the Q-Learning agent. Testing the agent_start, agent_step and agent_end.
    """
    def test_agent_start(self):

        test = {"num_actions": 4, "num_states": 2, "epsilon": 0.1, "step_size": 0.1, "discount": 1.0, "seed": 0}

        test_q_estimate = np.array([[0., 0., 0., 0.],
                                    [0., 0., 0., 0.]])
        test_action = 1

        test_agent = QLearningAgent()
        test_agent.agent_init(test)

        # Test that agent_start produces a preset action given a random seed
        self.assertEqual(test_agent.agent_start(0), test_action)

        # Test that agent_start maintains the initialized action-value estimates
        np.testing.assert_array_equal(test_agent.q, test_q_estimate)

    def test_agent_step(self):

        test = {"num_actions": 4, "num_states": 2, "epsilon": 0.1, "step_size": 0.1, "discount": 1.0, "seed": 0}

        test_q_estimate_1 = np.array([[0., 0.1, 0., 0.],
                                      [0., 0., 0., 0.]])
        test_q_estimate_2 = np.array([[0., 0.1, 0., 0.],
                                      [0., 0., 0., 0.01]])
        test_action_1 = 3
        test_action_2 = 1

        test_agent = QLearningAgent()
        test_agent.agent_init(test)

        # Set the agent to take the first state-action pair
        test_agent.agent_start(0)

        # Test that agent_step produces a preset action given a particular random seed
        self.assertEqual(test_agent.agent_step(1,1), test_action_1)
        # Test that agent_step produces the first action-value estimate update
        np.testing.assert_array_almost_equal(test_agent.q, test_q_estimate_1)

        # Test that agent_start produces a preset action given a particular random seed
        self.assertEqual(test_agent.agent_step(0,0), test_action_2)
        # Test that agent_start produces the second action-value estimate update
        np.testing.assert_array_almost_equal(test_agent.q, test_q_estimate_2)

    def test_agent_end(self):

        test = {"num_actions": 4, "num_states": 2, "epsilon": 0.1, "step_size": 0.1, "discount": 1.0, "seed": 0}

        test_q_estimate = np.array([[0., 0.19, 0., 0.],
                                    [0., 0., 0., 0.01]])

        test_agent = QLearningAgent()
        test_agent.agent_init(test)

        # Set the agent to take the first state-action pair
        test_agent.agent_start(0)
        test_agent.agent_step(1,1)
        test_agent.agent_step(0,0)
        test_agent.agent_end(1)

        # Test that the terminal state action-value estimate updates correctly
        np.testing.assert_array_almost_equal(test_agent.q, test_q_estimate)

if __name__ == '__main__':
    unittest.main()