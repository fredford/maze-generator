
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from src.agents.q_learning_agent import QLearningAgent
from src.agents.e_sarsa_agent import ExpectedSarsaAgent
from src.environments.env_cliffworld.cliffworld_env import CliffWorldEnv
from src.agents.agent_env_interactor import Interactor

def main():

    num_states =  48
    num_actions = 4
    epsilon = 0.1
    step_size = 0.5
    discount = 1.0
    seed = 0

    num_runs = 100
    num_episodes = 500

    all_reward_sums = {}
    all_state_visits = {}

    agent_info = {"num_actions": num_actions, "num_states": num_states, "epsilon": epsilon, "step_size": step_size, "discount": discount, "seed": seed}

    env = CliffWorldEnv()

    agents = {"Q-Learning": QLearningAgent, "Expected Sarsa": ExpectedSarsaAgent}
    agent_names = ["Q-Learning", "Expected Sarsa"]
    
    for agent_name in agent_names:
        
        all_reward_sums[agent_name] = []
        all_state_visits[agent_name] = []

        for run in tqdm(range(num_runs)):

            agent_info["seed"] = run

            interactor = Interactor(env, agents[agent_name], agent_info)
            
            reward_sums = []
            state_visits = np.zeros(48)

            for episode in range(num_episodes):
                if episode < num_episodes - 10:
                    interactor.episode(0)
                else:
                    state, action = interactor.start()
                    state_visits[state] += 1
                    isTerminal = False

                    while not isTerminal:
                        reward, state, action, isTerminal = interactor.step()
                        state_visits[state] += 1

                reward_sums.append(interactor.get_total_reward())

            all_reward_sums[agent_name].append(reward_sums)
            all_state_visits[agent_name].append(state_visits)

    for algorithm in ["Q-Learning", "Expected Sarsa"]:
        plt.plot(np.mean(all_reward_sums[algorithm], axis=0), label=algorithm)
    plt.xlabel("Episodes")
    plt.ylabel("Sum of\n rewards\n during\n episode",rotation=0, labelpad=40)
    plt.xlim(0,500)
    plt.ylim(-100,0)
    plt.legend()
    plt.show()

    for algorithm, position in [("Q-Learning", 211), ("Expected Sarsa", 212)]:
        plt.subplot(position)
        average_state_visits = np.array(all_state_visits[algorithm]).mean(axis=0)
        grid_state_visits = average_state_visits.reshape((4,12))
        grid_state_visits[0,1:-1] = np.nan
        plt.pcolormesh(grid_state_visits, edgecolors='gray', linewidth=2)
        plt.title(algorithm)
        plt.axis('off')
        cm = plt.get_cmap()
        cm.set_bad('gray')

        plt.subplots_adjust(bottom=0.0, right=0.7, top=1.0)
        cax = plt.axes([0.85, 0.0, 0.075, 1.])
    cbar = plt.colorbar(cax=cax)
    cbar.ax.set_ylabel("Visits during\n the last 10\n episodes", rotation=0, labelpad=70)
    plt.show()

main()