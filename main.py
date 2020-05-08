# Python External Modules
import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
from tqdm import tqdm
import sys

# Python Local Modules

# Import Agents
from src.agents.q_learning_agent import QLearningAgent
from src.agents.e_sarsa_agent import ExpectedSarsaAgent
from src.agents.agent_env_interactor import Interactor

# Import Maze
from src.environments.env_maze import maze as mg
from src.environments.env_maze.maze_env import MazeEnv

# Import Search
from src.searches.searches import Searches

# Import Utilities
from src.utils import Utils

def main():

    utility = Utils()

    board_size, window_size, booleansSearch, booleansSimulation, booleansOutput = utility.getParameters()
    
    showBFS = booleansSearch[0]
    showAstar = booleansSearch[1]

    runQL = booleansSimulation[0]
    runES = booleansSimulation[1]
    showQL = booleansSimulation[2]
    showES = booleansSimulation[3]

    if runQL or runES:
        epsilon = booleansSimulation[4]
        step_size = booleansSimulation[5]
        discount = booleansSimulation[6]
        num_episodes = booleansSimulation[7]
        num_runs = booleansSimulation[8]
        goal_reward = booleansSimulation[9]

    showRewards = booleansOutput[0]
    showHeatMap = booleansOutput[1]

    scale = window_size / board_size

    num_states = board_size * board_size
    num_actions = 4

    # Initialize Maze Environment
    maze = mg.Maze(board_size, board_size)
    env = MazeEnv(maze)

    # Initialize Search
    search = Searches(maze)
    search_lengths, search_visits, search_paths, search_colours = search.run_searches()

    # Initialize Simulations

    agents = {"Q-Learning": QLearningAgent, "Expected Sarsa": ExpectedSarsaAgent}
    simulations = []

    all_reward_sums = {}
    all_state_visits = {}
    all_states_visited = {}

    if runQL: simulations.append("Q-Learning")
    if runES: simulations.append("Expected Sarsa")

    if runQL or runES:
        for algorithm in simulations:
            all_states_visited[algorithm] = []
            all_state_visits[algorithm] = []
            all_reward_sums[algorithm] = []

            for run in tqdm(range(num_runs)):

                agent_info = {"num_actions": num_actions, "num_states": num_states, "epsilon": epsilon, "step_size": step_size, "discount": discount, "seed": run}

                interactor = Interactor(env, agents[algorithm], agent_info)

                reward_sums = []
                visited_list = []
                state_visits = np.zeros(num_states)

                for episode in range(num_episodes):
                    state, action = interactor.start()
                    state_visits[state] += 1
                    isTerminal = False

                    states_visited = []
                    
                    state_x, state_y = divmod(state, board_size)

                    states_visited.append((state_x, state_y))

                    step_num = 0

                    while not isTerminal:
                        reward, state, action, isTerminal = interactor.step()
                        
                        state_visits[state] += 1

                        state_x, state_y = divmod(state, board_size)

                        states_visited.append((state_x, state_y))
                        step_num += 1

                    visited_list.append(states_visited)
                    reward_sums.append(interactor.get_total_reward())

                all_states_visited[algorithm].append(visited_list)
                all_state_visits[algorithm].append(state_visits)
                all_reward_sums[algorithm].append(reward_sums)

    # Start Pygame engine
    if showBFS or showAstar or showQL or showES:
        pygame.init()

        clock = pygame.time.Clock()
        pygame.display.set_caption("Maze")
        screen = pygame.display.set_mode((window_size, window_size))



        runs = all_states_visited["Q-Learning"]

        #print(len(runs))
        #print(len(runs[0]))
        #print(len(runs[0][0]))
        #print(len(runs[0][0][0]))

        if len(runs) > 2:
            mid = len(runs)//2
        else:
            mid = -1

        count = 0
        for run in runs:

            for episode in run:

                if count == 0 or count == len(runs)-1 or count == mid:
                
                    for state in episode:

                        draw_grid(screen, scale, maze, window_size, search_paths, search_colours)
                        pygame.draw.rect(screen, (52,235,131), (state[0]*scale+(scale*3/10), state[1]*scale+(scale*3/10), (scale*(4/10)) , (scale*(4/10))))

                        clock.tick(200)
                        pygame.display.flip()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

            count += 1

    # Show rewards graph
    if showRewards:

        length_key = min(search_lengths.keys(), key=(lambda x: search_lengths[x]))
        length = search_lengths[length_key]
        best_case = float(-1.0*length)

        lowest = np.Inf
        highest = np.NINF

        for simulation in simulations:

            rewards = np.mean(all_reward_sums[simulation], axis=0)
            min_reward = min(rewards)
            max_reward = float(-1*length) + 20.0

            if min_reward < lowest:
                lowest = min_reward
            if max_reward > highest:
                highest = max_reward

            plt.plot(np.mean(all_reward_sums[simulation], axis=0), label=simulation)
        plt.hlines(best_case, 0, num_episodes, label="Length")
        plt.xlabel("Episodes")
        plt.ylabel("Sum of\n rewards\n during\n episode",rotation=0, labelpad=40)
        plt.xlim(0,num_episodes)
        plt.ylim(min_reward, max_reward)
        plt.legend()
        plt.show()

    if showHeatMap:
        for algorithm, position in [("Q-Learning", 211), ("Expected Sarsa", 212)]:
            plt.subplot(position)
            average_state_visits = np.array(all_state_visits[algorithm]).mean(axis=0)
            grid_state_visits = average_state_visits.reshape((board_size, board_size))
            corrected_vists = np.rot90(grid_state_visits)
            plt.pcolormesh(corrected_vists, edgecolors='gray', linewidth=2)
            plt.title(algorithm)
            plt.axis('off')
            cm = plt.get_cmap()
            cm.set_bad('gray')

            plt.subplots_adjust(bottom=0.0, right=0.7, top=1.0)
        
        cax = plt.axes([0.85, 0.0, 0.075, 1.])
        cbar = plt.colorbar(cax=cax)
        cbar.ax.set_ylabel("Visits during\n the last 10\n episodes", rotation=0, labelpad=70)
        plt.show()


    # End Pygame engine
    if showBFS or showAstar or showQL or showES:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()



def draw_grid(screen, scale, maze, window_size, search_paths, search_colours):
    cells = maze.maze
    screen.fill((255, 255, 255))

    for name in search_paths.keys():
        for cell in search_paths[name]:
            if cell != maze.start:
                if name == "astar":
                    pygame.draw.line(screen, search_colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.astar_previous.x*scale+(scale/2), cell.astar_previous.y*scale+(scale/2)))
                #elif name == "bfs":
                #    pygame.draw.line(screen, search_results.colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.bfs_previous.x*scale+(scale/2), cell.bfs_previous.y*scale+(scale/2)))

    pygame.draw.rect(screen, (0,0,255), (maze.start.x*scale+(scale/4), maze.start.y*scale+(scale/4), scale/2, scale/2))
    pygame.draw.rect(screen, (255,0,0), (maze.end.x*scale+(scale/4), maze.end.y*scale+(scale/4), scale/2, scale/2))

    for i in range(len(cells)+1):
        pygame.draw.line(screen, (0,0,0), (0,i*scale), (window_size,i*scale))

    for j in range(len(cells[0])+1):
        pygame.draw.line(screen, (0,0,0), (j*scale,0), (j*scale,window_size))

    for i in range(len(cells)):
        for j in range(len(cells[i])):

            cell = cells[i][j]

            for direction, value in cell.walls.items():
                if not value and direction == "above":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)) , ((scale*i)+scale-1, (scale*j)))
                if not value and direction == "below":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+1, (scale*j)+scale), ((scale*i)+scale-1, (scale*j)+scale))
                if not value and direction == "left":
                    pygame.draw.line(screen, (255,255,255), ((scale*i), (scale*j)+1), ((scale*i), (scale*j)+scale-1))
                if not value and direction == "right":
                    pygame.draw.line(screen, (255,255,255), ((scale*i)+scale, (scale*j)+1), ((scale*i)+scale, (scale*j)+scale-1))

    pygame.display.flip()



main()