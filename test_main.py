
# Python External Modules
import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
from tqdm import tqdm

# Python Local Modules

# Import Agents
from src.agents.q_learning_agent import QLearningAgent
from src.agents.agent_env_interactor import Interactor

# Import Maze
from src.environments.env_maze import maze as mg
from src.environments.env_maze.maze_env import MazeEnv

# Import Search
from src.searches.searches import Searches

def main():
    pygame.init()
    board_size = 10
    window_size = 600
    scale = window_size/board_size
    clock = pygame.time.Clock()

    pygame.display.set_caption("Maze")
    screen = pygame.display.set_mode((window_size, window_size))

    maze = mg.Maze(board_size, board_size)
    #search_results = Searches(maze)


    draw_grid(screen, scale, maze, window_size)
    #draw_graphs(screen, search_results, maze, scale, clock)


    num_states =  board_size * board_size
    num_actions = 4
    epsilon = 0.1
    step_size = 0.5
    discount = 1.0
    seed = 0

    num_episodes = 500
    num_runs = 100

    agent_info = {"num_actions": num_actions, "num_states": num_states, "epsilon": epsilon, "step_size": step_size, "discount": discount, "seed": seed}

    env = MazeEnv(board_size, maze)

    

    all_states_visited = []
    all_state_visits = []
    all_reward_sums = []

    for run in tqdm(range(num_runs)):

        agent_info = {"num_actions": num_actions, "num_states": num_states, "epsilon": epsilon, "step_size": step_size, "discount": discount, "seed": run}

        interactor = Interactor(env, QLearningAgent, agent_info)

        reward_sums = []
        state_visits = np.zeros(100)

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

            all_states_visited.append(states_visited)
            reward_sums.append(interactor.get_total_reward())

        all_state_visits.append(state_visits)
        all_reward_sums.append(reward_sums)

    """
    for run in range(num_runs):
        
        if run == 0:
            for episode in all_states_visited:
                for state in episode:

                    draw_grid(screen, scale, maze, window_size)
                    pygame.draw.rect(screen, (52,235,131), (state[0]*scale+(scale*3/10), state[1]*scale+(scale*3/10), (scale*(4/10)) , (scale*(4/10))))

                    clock.tick(200)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

        if run == 5:
            for episode in all_states_visited:
                for state in episode:

                    draw_grid(screen, scale, maze, window_size)
                    pygame.draw.rect(screen, (52,235,131), (state[0]*scale+(scale*3/10), state[1]*scale+(scale*3/10), (scale*(4/10)) , (scale*(4/10))))

                    clock.tick(200)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
        
        if run == num_runs-1:
            for episode in all_states_visited:
                for state in episode:

                    draw_grid(screen, scale, maze, window_size)
                    pygame.draw.rect(screen, (52,235,131), (state[0]*scale+(scale*3/10), state[1]*scale+(scale*3/10), (scale*(4/10)) , (scale*(4/10))))

                    clock.tick(200)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

    """

    plt.plot(np.mean(all_reward_sums, axis=0), label="Q-Learning")
    plt.xlabel("Episodes")
    plt.ylabel("Sum of\n rewards\n during\n episode",rotation=0, labelpad=40)
    plt.xlim(0,500)
    plt.ylim(-1000,0)
    plt.legend()
    plt.show()

    position = 211
    plt.subplot(position)
    average_state_visits = np.array(all_state_visits).mean(axis=0)
    grid_state_visits = average_state_visits.reshape((10,10))
    #grid_state_visits[0,1:-1] = np.nan
    #plt.pcolormesh(grid_state_visits, edgecolors='gray', linewidth=2)
    plt.title("Q-Learning")
    plt.axis('off')
    cm = plt.get_cmap()
    #cm.set_bad('gray')

    plt.subplots_adjust(bottom=0.0, right=0.7, top=1.0)
    cax = plt.axes([0.85, 0.0, 0.075, 1.])
    cbar = plt.colorbar(cax=cax)
    cbar.ax.set_ylabel("Visits during\n the last 10\n episodes", rotation=0, labelpad=70)
    plt.show()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def draw_graphs(screen, search_results, maze, scale, clock):

    for name in search_results.paths.keys():
        for cell in search_results.paths[name]:
            if cell != maze.start:
                if name == "astar path":
                    pygame.draw.line(screen, search_results.colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.astar_previous.x*scale+(scale/2), cell.astar_previous.y*scale+(scale/2)))
                #elif name == "bfs path":
                #    pygame.draw.line(screen, search_results.colours[name], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.bfs_previous.x*scale+(scale/2), cell.bfs_previous.y*scale+(scale/2)))

            clock.tick(10)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

def draw_grid(screen, scale, maze, window_size):
    cells = maze.maze
    screen.fill((255, 255, 255))

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