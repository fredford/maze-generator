import sys
import copy
import numpy as np
import pygame as pg
from tqdm import tqdm

from src.button import Button
from src.maze import Maze
from src.generator import Generator
from src.searcher import Searcher
from src.agent_env_interactor import Interactor
from src.q_learning_agent import QLearningAgent
from src.e_sarsa_agent import ExpectedSarsaAgent

from src.maze_env import MazeEnv

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 111, 255)
ORANGE = (255, 128, 0)
DARK_ORANGE = (199, 99, 0)
PURPLE = (128, 0, 255)
PINK = (255, 130, 253)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
DARK_GREY = (110, 110, 110)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)

class Utils:
    """Object used to handle the GUI interactions with the generation processes, search algorithms and reinforcement learning agents and graphically display the results.
    """

    def __init__(self, window_height, window_width, button_height, screen):
        
        # Window parameters
        self.window_height = window_height
        self.window_width  = window_width
        self.button_height = button_height
        self.screen  = screen
        self.buttons = None
        self.clock = pg.time.Clock()

        # Maze parameters
        self.maze_size = 10
        self.scale = (self.window_width/self.maze_size)
        self.maze = Maze(self.maze_size, self.scale)
        self.maze_list = [self.maze.grid]
        self.build_maze = copy.deepcopy(self.maze.grid)
        
        # Initialize searcher, generator, learner objects
        self.generator = Generator()    # Used to generate mazes
        self.searcher = Searcher()      # Used to search mazes
        #self.learner = Learner()        # Used to simulate learning on mazes

        # Paths searched
        self.paths = {}
        self.shown_path = {}
        # Number of cells visited in each search
        self.visits = {"BFS": "-", "A*":"-", "DFS": "-"}
        # Length of the path found from the start to the end
        self.lengths = {"BFS": "-", "A*":"-", "DFS": "-"}

        # Reinforcement Learning parameters
        self.num_actions = 4
        self.num_states = self.maze.size * self.maze.size
        self.step_size = 0.1
        self.epsilon = 0.1
        self.discount = 0.1
        self.num_episodes = 50
        self.num_runs = 5
        self.all_states_visited = {}
        self.all_state_visits = {}
        self.all_reward_sums = {}

        # Colors
        self.path_colors = {
            "BFS": RED,
            "A*": ORANGE,
            "DFS": PINK,
            "Explore_BFS": DARK_GREEN,
            "Explore_A*": DARK_ORANGE,
            "Explore_DFS": PURPLE
            }

    def create_buttons(self):
        """Method to create buttons to be used in the GUI
        """
        # Row sizing
        row0 = self.window_height-(self.button_height*5)
        row1 = row0 + self.button_height
        row2 = row0 + self.button_height*2
        row3 = row0 + self.button_height*3
        row4 = row0 + self.button_height*4

        # Column sizing
        title_width = self.window_width/6
        column0_x = 0
        column1_x = self.window_width*1/6
        column2_x = self.window_width*2/6
        column3_x = self.window_width*2/6 + (2/3)*title_width - 1
        column4_x = self.window_width*3/6 - 2
        column5_x = self.window_width*3/6 + (1/3)*title_width - 2
        column6_x = column5_x + title_width*8/6-1

        column0_width = self.window_width/6
        column1_width = self.window_width/6
        column2_width = title_width*2/3
        column3_width = title_width/3
        column4_width = title_width/3
        column5_width = (title_width * 4/6)*2
        column6_width = self.window_width-column6_x

        column0a_width = column0_width/4
        column0b_width = column0_width/2
        column0c_width = column0_width/4 + 1
        column0b_x = column0_x  + column0a_width
        column0c_x = column0b_x + column0b_width - 1
        
        column1b_x = column1_x  + column0a_width
        column1c_x = column1b_x + column0b_width - 1

        column5a_width = title_width * 4/6 + 2
        column5c_width = column5a_width/4
        column5d_width = column5a_width/2
        column5e_width = column5a_width/4

        column5b_x = column5_x + column5a_width - 1
        column5d_x = column5b_x + column5c_width - 1
        column5e_x = column5d_x + column5d_width

        column6a_width = column6_width/2
        column6b_width = column6_width/8
        column6c_width = column6_width/4 + 2

        column6b_x = column6_x + column6_width/2
        column6c_x = column6b_x + column6b_width - 1
        column6d_x = column6c_x + column6c_width

        self.titles = {
            # Titles
            "Generate": Button(DARK_GREY, column0_x, row0, column0_width, self.button_height, "Generate"),
            "Options1": Button(DARK_GREY, column1_x, row0, column1_width, self.button_height, "Options"),
            "Search":   Button(DARK_GREY, column2_x, row0, column2_width, self.button_height, "Search"),      
            "Length":   Button(DARK_GREY, column3_x, row0, column3_width, self.button_height, "Length"),
            "Visits":   Button(DARK_GREY, column4_x, row0, column4_width, self.button_height, "Visits"),
            "Simulate": Button(DARK_GREY, column5_x, row0, column5_width, self.button_height, "Simulate"),
            "Options2": Button(DARK_GREY, column6_x, row0, column6_width, self.button_height, "Options"),
            # Maze Length buttons
            "lengthA*":   Button(GREY, column3_x, row1, column3_width, self.button_height, str('-')),
            "lengthBFS":  Button(GREY, column3_x, row2, column3_width, self.button_height, str('-')),
            "lengthDFS":  Button(GREY, column3_x, row3, column3_width, self.button_height, str('-')),
            "lengthBlank":Button(GREY, column3_x, row4, column3_width, self.button_height, ""),
            # Maze Visits buttons
            "visitsA*":   Button(GREY, column4_x, row1, column4_width, self.button_height, str('-')),
            "visitsBFS":  Button(GREY, column4_x, row2, column4_width, self.button_height, str('-')), 
            "visitsDFS":  Button(GREY, column4_x, row3, column4_width, self.button_height, str('-')),
            "visitsBlank":Button(GREY, column4_x, row4, column4_width, self.button_height, ""),
            # Reinforcement Learning parameter buttons
            "step_size":      Button(GREY, column5_x, row2, column5a_width, self.button_height, "Step Size:"),
            "epsilon":        Button(GREY, column5_x, row3, column5a_width, self.button_height, "Epsilon:"),
            "discount":       Button(GREY, column5_x, row4, column5a_width, self.button_height, "Discount:"),
            "Size":           Button(GREY, column1b_x, row2, column0b_width, self.button_height, str(self.maze_size)),
            "stepDisplay":    Button(GREY, column5d_x, row2, column5d_width, self.button_height, str(self.step_size)),
            "epsilonDisplay": Button(GREY, column5d_x, row3, column5d_width, self.button_height, str(self.epsilon)),
            "discountDisplay":Button(GREY, column5d_x, row4, column5d_width, self.button_height, str(self.discount)),
            "dispEpisode":    Button(GREY, column6c_x, row1, column6c_width, self.button_height, str(self.num_episodes)),
            "dispRuns":       Button(GREY, column6c_x, row2, column6c_width, self.button_height, str(self.num_runs)),
        }

        self.buttons = {
            # Maze generation buttons
            "genDFS":   Button(GREY, column0_x , row1, column0_width , self.button_height, "DFS"),     
            "Prims":    Button(GREY, column0_x , row2, column0_width , self.button_height, "Prims"),
            "Recursive":Button(GREY, column0_x , row3, column0_width , self.button_height, "Recursive"),
            "Start":    Button(GREY, column0_x , row4, column0a_width, self.button_height, "S"),
            "Click":    Button(GREY, column0b_x, row4, column0b_width, self.button_height, "Click"),
            "End":      Button(GREY, column0c_x, row4, column0c_width, self.button_height, "E"),
            # Maze Options
            "Maze Size":Button(GREY, column1_x , row1, column1_width , self.button_height, "Maze Size"),
            "Minus":    Button(GREY, column1_x , row2, column0a_width, self.button_height, "-"),
            "Plus":     Button(GREY, column1c_x, row2, column0c_width, self.button_height, "+"),
            "Build":    Button(GREY, column1_x , row3, column1_width , self.button_height, "Show Build"),
            "Explore":  Button(GREY, column1_x , row4, column1_width , self.button_height, "Show Explore"),
            # Maze searching buttons
            "A*":       Button(GREY, column2_x, row1, column2_width, self.button_height, "A*"),
            "BFS":      Button(GREY, column2_x, row2, column2_width, self.button_height, "BFS"),
            "DFS":      Button(GREY, column2_x, row3, column2_width, self.button_height, "DFS"),
            "Blank":    Button(GREY, column2_x, row4, column2_width, self.button_height, ""),
            # Reinforcement Learning
            "Q-Learning":     Button(GREY, column5_x , row1, column5a_width, self.button_height, "Q-Learning"),
            "Expected SARSA": Button(GREY, column5b_x, row1, column5a_width, self.button_height, "Exp. SARSA"),
            "stepMinus":      Button(GREY, column5b_x, row2, column5c_width, self.button_height, "-"), 
            "stepPlus":       Button(GREY, column5e_x, row2, column5e_width, self.button_height, "+"),             
            "epsilonMinus":   Button(GREY, column5b_x, row3, column5c_width, self.button_height, "-"),
            "epsilonPlus":    Button(GREY, column5e_x, row3, column5e_width, self.button_height, "+"),
            "discountMinus":  Button(GREY, column5b_x, row4, column5c_width, self.button_height, "-"),
            "discountPlus":   Button(GREY, column5e_x, row4, column5e_width, self.button_height, "+"),
            # RL Options
            "Num Episodes":Button(GREY, column6_x , row1, column6a_width, self.button_height, "Episodes:"),
            "minusEpisode":Button(GREY, column6b_x, row1, column6b_width, self.button_height, "-"),
            "plusEpisode": Button(GREY, column6d_x, row1, column6b_width, self.button_height, "+"),
            "Num Runs":    Button(GREY, column6_x , row2, column6a_width, self.button_height, "Runs:"),
            "minusRun":    Button(GREY, column6b_x, row2, column6b_width, self.button_height, "-"),
            "plusRun":     Button(GREY, column6d_x, row2, column6b_width, self.button_height, "+"),
            "Heat Map":    Button(GREY, column6_x , row3, column6a_width, self.button_height, "Heat Map"),
            "Show Run":    Button(GREY, column6b_x, row3, column6a_width, self.button_height, "Show Run"),
            "Reset":       Button(RED , column6_x , row4, column6_width , self.button_height, "Reset")
        }               

    def draw_window(self):
        """This method is called to display the contents created onto the window. First by updating the values displayed by the buttons, then providing a background for the maze, the background currently set for each cell in the grid if a heat map is showing, then displaying the current layout of the cells on the grid, then printing any generated pathways searched, and finally if selected displaying a select number of episodes from running a reinforcement learning algorithm.
        """
        # Draw the title buttons with updated values, buttons that can't be pressed
        for key, value in self.titles.items():
            if key == "lengthA*":
                value.text = str(self.lengths["A*"])
            elif key == "lengthBFS":
                value.text = str(self.lengths["BFS"])
            elif key == "lengthDFS":
                value.text = str(self.lengths["DFS"])
            elif key == "visitsA*":
                if self.visits["A*"] == '-':
                    value.text = str(self.visits["A*"])
                else:
                    value.text = str(len(self.visits["A*"]))
            elif key == "visitsBFS":
                if self.visits["BFS"] == '-':
                    value.text = str(self.visits["BFS"])
                else:
                    value.text = str(len(self.visits["BFS"]))
            elif key == "visitsDFS":
                if self.visits["DFS"] == '-':
                    value.text = str(self.visits["DFS"])
                else:
                    value.text = str(len(self.visits["DFS"]))
            elif key == "Size":
                value.text = str(self.maze_size)
            elif key == "epsilonDisplay":
                value.text = "%.2f" % self.epsilon
            elif key == "stepDisplay":
                value.text = "%.2f" % self.step_size
            elif key == "discountDisplay":
                value.text = "%.2f" % self.discount
            elif key == "dispEpisode":
                value.text = str(self.num_episodes)
            elif key == "dispRuns":
                value.text = str(self.num_runs)
        
            value.draw(self.screen, BLACK)

        # Draw the buttons that can be pressed by the user
        for key, value in self.buttons.items():
            value.draw(self.screen, BLACK)

        scale = self.window_width / self.maze_size
        font = pg.font.SysFont("arial", int(scale/2))

        # Draw maze background
        pg.draw.rect(self.screen, WHITE, (0,0,self.window_width, self.window_height-125))

        if self.buttons["Build"].status and self.buttons["Click"].pressed == 0:
            print_maze = self.build_maze
        else:
            print_maze = self.maze.grid
        
        for i in range(len(print_maze)):
            for j in range(len(print_maze[i])):
                cell = print_maze[i][j]
                
                pg.draw.rect(self.screen, cell.border, (scale*i+1, scale*j+1, scale-1, scale-1))
                pg.draw.rect(self.screen, cell.background, (scale*i+(scale/10), scale*j+(scale/10), scale-(scale*2/10), scale-(scale*2/10)))

                for direction, value in cell.walls.items():
                    if value and direction == "above":
                        pg.draw.line(self.screen, BLACK, ((scale*i)+1, (scale*j)), ((scale*i)+scale-1, (scale*j)))
                    if value and direction == "below":
                        pg.draw.line(self.screen, BLACK, ((scale*i)+1, (scale*j)+scale),((scale*i)+scale-1, (scale*j)+scale))
                    if value and direction == "left":
                        pg.draw.line(self.screen, BLACK, ((scale*i), (scale*j)+1),((scale*i), (scale*j)+scale-1))
                    if value and direction == "right":
                        pg.draw.line(self.screen, BLACK, ((scale*i)+scale, (scale*j)+1),((scale*i)+scale, (scale*j)+scale-1))

                if cell.isStart:
                    text = font.render("S", 1, (0, 0, 0))
                    self.screen.blit(text, (scale*i + scale/2 - text.get_width()/2, scale*j + scale/2 - text.get_height()/2))
                elif cell.isEnd:
                    text = font.render("E", 1, (0, 0, 0))
                    self.screen.blit(text, (scale*i + scale/2 - text.get_width()/2, scale*j + scale/2 - text.get_height()/2))

        self.print_path(self.shown_path)
        self.print_path(self.paths)

        if self.buttons["Show Run"].status:
            pg.draw.rect(self.screen, GREEN, (self.state[0]*self.scale+(self.scale*3/10), self.state[1]*self.scale+(self.scale*3/10), (self.scale*(4/10)) , (self.scale*(4/10))))

        pg.display.flip()

    def handle_event(self, event_key):
        """This method handles processing the event key generated when the user clicked on the GUI. Selecting the appropriate button functionality associated to the event key generated.

        Arguments:
            event_key {string} -- String associated to the button that was pressed in the GUI.
        """

        # When the user clicks on a plus or minus button on the GUI
        if event_key == "stepPlus"     or event_key == "discountPlus"  or event_key == "epsilonPlus" or \
           event_key == "plusEpisode"  or event_key == "plusRun"       or event_key == "Plus" or \
           event_key == "stepMinus"    or event_key == "discountMinus" or event_key == "epsilonMinus" or \
           event_key == "minusEpisode" or event_key == "minusRun"      or event_key == "Minus" \
           and self.buttons[event_key].pressed == 1:
    
            self.buttons[event_key].color = LIGHT_BLUE
            self.draw_window()
            if event_key == "stepPlus" and self.step_size < 1.0:
                self.step_size += 0.01
            elif event_key == "stepMinus" and self.step_size > 0.01:
                self.step_size -= 0.01
            elif event_key == "discountPlus" and self.discount < 1.0:
                self.discount += 0.01
            elif event_key == "discountMinus" and self.discount > 0.01:
                self.discount -= 0.01
            elif event_key == "epsilonPlus" and self.epsilon < 1.0:
                self.epsilon += 0.01
            elif event_key == "epsilonMinus" and self.epsilon > 0.01:
                self.epsilon -= 0.01
            elif event_key == "plusEpisode" and self.num_episodes < 200:
                self.num_episodes += 5
            elif event_key == "minusEpisode" and self.num_episodes > 5:
                self.num_episodes -= 5
            elif event_key == "plusRun" and self.num_runs < 50:
                self.num_runs += 1
            elif event_key == "minusRun" and self.num_runs > 1:
                self.num_runs -= 1
            elif event_key == "Plus" and self.maze_size < 60:
                self.maze_size += 2
                self.scale = self.window_width / self.maze_size
                self.maze = Maze(self.maze_size, self.scale)
                self.build_maze = copy.deepcopy(self.maze.grid)
            elif event_key == "Minus" and self.maze_size > 2:
                self.maze_size -= 2
                self.scale = self.window_width / self.maze_size
                self.maze = Maze(self.maze_size, self.scale)
                self.build_maze = copy.deepcopy(self.maze.grid)
            self.buttons[event_key].color = GREY
            self.buttons[event_key].pressed = 0

        # When the user clicks the Reset button, the maze will be reset to the original conditions
        if self.buttons["Reset"].pressed == 1:
            self.maze = Maze(self.maze_size, self.scale)
            self.build_maze = copy.deepcopy(self.maze.grid)

            self.reset_maze()
            # Reset the status of each button in the GUI
            for key, button in self.buttons.items():
                if key != "Reset":
                    button.pressed = 0
                    button.color = GREY
                    button.status = False
                else:
                    button.pressed = 0   

        # When the user clicks a maze generating button
        if event_key == "genDFS" or event_key == "Prims" or event_key == "Recursive":
            if self.buttons[event_key].pressed == 1:
                self.buttons[event_key].color = LIGHT_BLUE

                # Clear the maze walls to show the recursive process
                if event_key == "Recursive":
                    self.clear_maze()
                # Send the current grid to the generator
                self.generator.get_grid(self.maze.grid)
                
                # Pass the event key to the generator and run the selected option
                try:
                    maze_list = self.generator.run_generator(event_key)
                    self.maze.grid = copy.deepcopy(self.generator.temp_maze)
                except Exception as e:
                    print(e)

                # Update the start and end cells for the updated maze created
                self.maze.update_start_end()
                # If the maze is recursive it requires having walls set and removed
                if self.buttons["Build"].status and event_key == "Recursive":
                    for temp_current_cell, temp_next_cell, status in maze_list:
                        current_cell = self.build_maze[temp_current_cell.x][temp_current_cell.y]
                        next_cell = self.build_maze[temp_next_cell.x][temp_next_cell.y]
                        if status == "wall":
                            current_cell.set_wall(next_cell)
                            next_cell.set_wall(current_cell)
                        else:
                            current_cell.set_path(next_cell)
                            next_cell.set_path(current_cell)
                        self.draw_window()
                # DFS and Prims only require having walls removed
                elif self.buttons["Build"].status:
                    self.iterate_build_maze(maze_list)
                # Set the event button to an on state
                self.buttons[event_key].pressed = 2
            # When the user clicks the button to turn it off
            elif self.buttons[event_key].pressed == 3:
                self.buttons[event_key].color = GREY
                self.buttons[event_key].pressed = 0
                self.reset_maze()
        # When the user clicks the "S" or "E" buttons, to select a new start point or end point
        if event_key == "Start" or event_key == "End" and self.buttons[event_key].pressed == 1:
            self.buttons[event_key].color = LIGHT_BLUE
            running = True
            while running:
                self.draw_window()
                event = pg.event.poll()
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONUP:

                    for row in self.maze.grid:
                        for cell in row:
                            if cell.select(event.pos):
                                if event_key == "Start":
                                    self.maze.change_start(cell)
                                elif event_key == "End":
                                    self.maze.change_end(cell)
                                running = False
            self.buttons[event_key].color = GREY
            self.buttons[event_key].pressed = 0
        
        # When the user selects the option to show maze exploration, the cells visited in the search process
        if self.buttons["Explore"].pressed == 1:
            self.buttons["Explore"].color = LIGHT_BLUE
        else:
            self.buttons["Explore"].color = GREY
            self.buttons["Explore"].pressed = 0
        
        # When the "Click" button is not pressed
        if self.buttons["Click"].pressed == 0:
            # If the "Build" button is pressed to illuminate
            if self.buttons["Build"].pressed == 1:
                self.buttons["Build"].color = LIGHT_BLUE
                self.buttons["Build"].status = True
            # If the "Build" button is pressed again to turn off
            elif self.buttons["Build"].pressed == 2:
                self.buttons["Build"].status = False
                self.buttons["Build"].pressed = 0
                self.buttons["Build"].color = GREY
        
        # When the "Click" button is pressed
        elif self.buttons["Click"].pressed == 1:
            self.buttons["Click"].color = LIGHT_BLUE
            self.clear_maze()   # Clear the walls from the maze

            # Allow the user to continue to select cells to build a wall around
            while True:
                self.draw_window()
                event = pg.event.poll()
                if event.type == pg.QUIT:
                    sys.exit()
                # When an mousebutton event has been registered
                elif event.type == pg.MOUSEBUTTONUP:
                    # When the click button is pressed
                    if self.buttons["Click"].select(event.pos):
                        break
                    # Check if a cell has been selected
                    for row in self.maze.grid:
                        for cell in row:
                            if cell.select(event.pos):
                                cell.changeBackground()

            # Turn off the "Click" button
            self.buttons["Click"].color = GREY
            self.buttons["Click"].pressed = 0
            self.buttons["Click"].status = True

        # When the user clicks on the Show Run button to show the process of the agent running through the grid
        if self.buttons["Show Run"].pressed == 1 and (self.buttons["Q-Learning"].pressed == 2 or self.buttons["Expected SARSA"].pressed == 2):
            self.buttons["Show Run"].color = LIGHT_BLUE
            self.buttons["Show Run"].status = True
            
            if self.buttons["Q-Learning"].pressed == 2:
                runs = self.all_states_visited["Q-Learning"]
            else:
                runs = self.all_states_visited["Expected SARSA"]

            # Set the mid point of the runs performed by the agent
            if len(runs) > 2:
                mid = len(runs)//2
            else:
                mid = -1

            count = 0
            # Go through each run and display the first set of episodes, the middle set of episodes and the final set of episodes.
            for run in runs:
                for episode in run:
                    if count == 0 or count == len(runs)-1 or count == mid:
                        for self.state in episode:
                            self.draw_window()
                count += 1
            self.buttons["Show Run"].pressed = 2
        # Reset the Show Run button
        elif self.buttons["Show Run"].pressed == 3:
            self.buttons["Show Run"].color = GREY
            self.buttons["Show Run"].pressed = 0
            self.buttons["Show Run"].status = False

        # When the user clicks the Heat Map button, show the heat map of the average visits made by the agent on each state. 
        if self.buttons["Heat Map"].pressed == 1 and (self.buttons["Q-Learning"].pressed == 2 or self.buttons["Expected SARSA"].pressed == 2):
            self.buttons["Heat Map"].color = LIGHT_BLUE

            if self.buttons["Q-Learning"].pressed == 2:
                average_state_visits = np.array(self.all_state_visits["Q-Learning"]).mean(axis=0)
            else:
                average_state_visits = np.array(self.all_state_visits["Expected SARSA"]).mean(axis=0)


            max_visit = np.max(average_state_visits[np.nonzero(average_state_visits)])
            min_visit = np.min(average_state_visits[np.nonzero(average_state_visits)])

            visit_range = max_visit - min_visit

            for state, visits in enumerate(average_state_visits):
                state_x, state_y = divmod(state, self.maze_size)
                cell = self.maze.grid[state_x][state_y]
                if cell.background != BLACK and not cell.isStart and not cell.isEnd:
                    if visits != 0:
                        cell.background = (255-((visits-min_visit)/visit_range)*255, 255, 255-((visits-min_visit)/visit_range)*255)
                    else:
                        cell.background = WHITE

            self.buttons["Heat Map"].pressed = 2

        # Reset the Heat Map button
        elif self.buttons["Heat Map"].pressed == 3:
            self.buttons["Heat Map"].color = GREY
            for row in self.maze.grid:
                for cell in row:
                    if cell.background != BLACK and not cell.isStart and not cell.isEnd:
                        cell.background = WHITE
            self.buttons["Heat Map"].pressed = 0
            

        # The user cannot select a search algorithm without first generating a maze or grid
        if self.buttons["genDFS"].pressed == 2 or self.buttons["Prims"].pressed == 2 or \
           self.buttons["Recursive"].pressed == 2 or self.buttons["Click"].status == True:
            # When the user clicks on a search algorithm button
            if event_key == "BFS" or event_key == "A*" or event_key == "DFS":
                if self.buttons[event_key].pressed == 1:
                    self.buttons[event_key].color = LIGHT_BLUE
                    # Pass the locations of the start and end points to the searcher
                    self.searcher.get_grid(self.maze.start, self.maze.end)
                    # From the provided event key determine which search method to use
                    if event_key == "BFS":
                        self.searcher.run_BFS()
                    elif event_key == "A*":
                        self.searcher.run_Astar()
                    elif event_key == "DFS":
                        self.searcher.run_DFS()
                    # Acquire the output information found by the search algorithm
                    self.paths[event_key] = self.searcher.paths[event_key]
                    self.visits[event_key] = self.searcher.visits[event_key]
                    self.lengths[event_key] = self.searcher.lengths[event_key]

                    # If the user chose to display the exploration process add the paths visited to be shown
                    if self.buttons["Explore"].pressed == 1:
                        self.buttons[event_key].color = LIGHT_BLUE
                        self.shown_path["Explore_" + event_key] = []

                        # Iterate through each cell as it is visited
                        for current in self.visits[event_key]:
                            self.shown_path["Explore_" + event_key].append(current)
                            self.draw_window()
                    self.buttons[event_key].pressed = 2
                # When the user turns off the search algorithm reset the information for that algorithm
                elif self.buttons[event_key].pressed == 3:
                    self.buttons[event_key].color = GREY
                    self.buttons[event_key].pressed = 0
                    self.shown_path["Explore_"+event_key] = None
                    self.paths[event_key] = None
                    self.visits[event_key] = "-"
                    self.lengths[event_key] = "-"
            # When the user clicks on a reinforcement learning button
            if event_key == "Q-Learning" or event_key == "Expected SARSA" and self.buttons[event_key].pressed == 1:
                if event_key == "Q-Learning" and self.buttons["Expected SARSA"].pressed == 2:
                    self.buttons["Expected SARSA"].color = GREY
                    self.buttons["Expected SARSA"].pressed = 0
                    self.all_states_visited["Expected SARSA"] = []
                    self.all_state_visits["Expected SARSA"] = []
                    self.all_reward_sums["Expected SARSA"] = []
                elif event_key == "Expected SARSA" and self.buttons["Q-Learning"].pressed == 2:
                    self.buttons["Q-Learning"].color = GREY
                    self.buttons["Q-Learning"].pressed = 0
                    self.all_states_visited["Q-Learning"] = []
                    self.all_state_visits["Q-Learning"] = []
                    self.all_reward_sums["Q-Learning"] = []
                self.num_states = self.maze.size * self.maze.size
                env = MazeEnv(self.maze)
                agents = {"Q-Learning": QLearningAgent, "Expected SARSA": ExpectedSarsaAgent}

                self.all_states_visited[event_key] = []
                self.all_state_visits[event_key] = []
                self.all_reward_sums[event_key] = []

                # Perform each run of the specified set of runs
                for run in tqdm(range(self.num_runs)):

                    agent_info = {"num_actions": self.num_actions, "num_states": self.num_states, "epsilon": self.epsilon, "step_size": self.step_size, "discount": self.discount, "seed": run}

                    interactor = Interactor(env, agents[event_key], agent_info)

                    reward_sums = []
                    visited_list = []
                    state_visits = np.zeros(self.num_states)

                    # Perform each episode of the specified number of episodes
                    for episode in range(self.num_episodes):
                        state, action = interactor.start()
                        state_visits[state] += 1
                        isTerminal = False

                        states_visited = []
                        
                        state_x, state_y = divmod(state, self.maze_size)

                        states_visited.append((state_x, state_y))

                        step_num = 0
                        # Continue performing steps in the episode until the agent reaches the terminal state.
                        while not isTerminal:
                            reward, state, action, isTerminal = interactor.step()
                            
                            state_visits[state] += 1

                            state_x, state_y = divmod(state, self.maze_size)

                            states_visited.append((state_x, state_y))
                            step_num += 1

                        visited_list.append(states_visited)
                        reward_sums.append(interactor.get_total_reward())

                    # Append the collected data to the outcome lists to be used in displaying the outcome of the learning simulation
                    self.all_states_visited[event_key].append(visited_list)
                    self.all_state_visits[event_key].append(state_visits)
                    self.all_reward_sums[event_key].append(reward_sums)
                    
                self.buttons[event_key].pressed = 2
            
            # Reset the reinforcement learning button
            elif event_key == "Q-Learning" or event_key == "Expected SARSA" and self.buttons[event_key].pressed == 3:
                self.buttons[event_key].color = GREY
                self.buttons[event_key].pressed = 0
                self.all_states_visited[event_key] = []
                self.all_state_visits[event_key] = []
                self.all_reward_sums[event_key] = []

    def iterate_build_maze(self, maze_list):
        """This method iterates through each step in building the maze to display the process used.

        Arguments:
            maze_list {list} -- List of tuples (current_cell, next_cell) representing the walls removed from each cell pairing or edge. Cells are Cell objects.
        """

        for temp_current_cell, temp_next_cell in maze_list:
            current_cell = self.build_maze[temp_current_cell.x][temp_current_cell.y]
            next_cell = self.build_maze[temp_next_cell.x][temp_next_cell.y]
            current_cell.set_path(next_cell)
            next_cell.set_path(current_cell)
            self.draw_window()

    def reset_maze(self):
        """This method resets the conditions of the maze and removes all paths, visits and lengths established, as well as replacing all walls.
        """
        self.maze = Maze(self.maze_size, self.scale)
        self.build_maze = copy.deepcopy(self.maze.grid)
        
        self.buttons["Click"].status = False

        for key, path in self.paths.items():
            path = None
        for key, path in self.shown_path.items():
            path = None
        for key, visit in self.visits.items():
            visit = "-"
        for key, length in self.lengths.items():
            length = "-"

    def clear_maze(self):
        """This method clears the walls from all cells in the maze.
        """

        clear_list = [self.maze.grid, self.build_maze]
        for grid in clear_list:
            for row in grid:
                for cell in row:
                    if cell.background != BLACK:
                        for direction, wall in cell.walls.items():
                            if wall:
                                cell.walls[direction] = False

    def print_path(self, path_dict):
        """This method draws all paths in the dictionary provided to the pygame screen.

        Arguments:
            path_dict {dict} -- Dictionary of paths to be displayed in the format of cell objects in a list
        """

        scale = self.window_width / self.maze_size

        for search, path in path_dict.items():
            if path != None:
                for cell in path:
                    if cell != self.maze.start:
                        pg.draw.line(self.screen, self.path_colors[search], (cell.x*scale+(scale/2), cell.y*scale+(scale/2)),(cell.get_previous(search).x*scale+(scale/2), cell.get_previous(search).y*scale+(scale/2)))