import sys


class Utils():

    def getParameters(self):

        print("Maze Solver v1.0 by Fraser Redford\n"
            "----------------------------------")
        print("This program offers the following functionality:\n"
            "Search\n"
            "- Breadth First Search - Exhaustive search for the goal node\n"
            "- A* Search            - Heuristic search for the goal node\n"
            "Simulation\n"
            "- Q-Learning           - Epsilon-Greedy action-selection agent\n"
            "- Expected Sarsa       - Weighted sum expected value convergence agent\n"
            "Output\n"
            "- Show simulation sum of rewards"
            "- Show visited states heat map"
            "- Show maze run through")
        print("Window Parameters\n"
            "-----------------")

        inputParameters = True

        while inputParameters:
            
            input_board = input("Board Size (2-100; default=10): ")
            
            if input_board == "q" or input_board == "Q":
                print("Quitting!")
                sys.exit(0)

            elif input_board == "":
                input_board = "10"
            
            try:
                board_size = int(input_board)

                if board_size > 100 or board_size < 2:
                    raise Exception
            except:
                print("Invalid board size!")
                continue
            
            input_window = input("Window Size (100-1000; default=600): ")

            if input_window == "q" or input_window == "Q":
                print("Quitting!")
                sys.exit(0)

            elif input_window == "":
                input_window = "600"
            
            try:
                window_size = int(input_window)

                if window_size > 1000 or window_size < 100:
                    continue
            except:
                print("Invalid window size!")
                continue

            inputParameters = False

        print("Search\n"
              "------")

        booleansSearch = []

        for string in ["Show BFS (y/n): ",  "Show A* (y/n): ", ]:
            booleansSearch.append(self.boolean_check(string))

        print("Simulation\n"
              "----------")

        booleansSimulation = []

        for string in ["Q-Learning (y/n): ", "Expected Sarsa (y/n): "]:
            booleansSimulation.append(self.boolean_check(string))

        if booleansSimulation[0]:
            booleansSimulation.append(self.boolean_check("Show Q-Learning simulating (y/n): "))
        else:
            booleansSimulation.append(False)
        if booleansSimulation[1]:
            booleansSimulation.append(self.boolean_check("Show Expected Sarsa simulating (y/n): "))
        else:
            booleansSimulation.append(False)

        if booleansSimulation[0] or booleansSimulation[1]:
            while True:
                input_epsilon = input("Epsilon ([0-1], exploration rate, default=0.1): ")
                
                if input_epsilon.lower() == "q":
                    print("Quitting")
                    sys.exit(0)
                elif input_epsilon == "":
                    booleansSimulation.append(0.1)
                    break

                try:
                    epsilon = float(input_epsilon)

                    if epsilon >= 0.0 and epsilon <= 1.0:
                        booleansSimulation.append(epsilon)
                        break
                    else:
                        raise Exception
                except:
                    print("Invalid input!")

            while True:
                input_step = input("Step Size ([0-1], amount the action-value will update, default=0.5): ")
                
                if input_step.lower() == "q":
                    print("Quitting")
                    sys.exit(0)
                elif input_step == "":
                    booleansSimulation.append(0.5)
                    break

                try:
                    step_size = float(input_step)

                    if step_size >= 0.0 and step_size <= 1.0:
                        booleansSimulation.append(step_size)
                        break
                    else:
                        raise Exception
                except:
                    print("Invalid input!")

            while True:
                input_discount = input("Discount ([0-1], 0 is near-sighted rewards 1 is far-sighted rewards, default=1): ")
                
                if input_discount.lower() == "q":
                    print("Quitting")
                    sys.exit(0)
                elif input_discount == "":
                    booleansSimulation.append(1.0)
                    break

                try:
                    discount = float(input_discount)

                    if discount >= 0.0 and discount <= 1.0:
                        booleansSimulation.append(discount)
                        break
                    else:
                        raise Exception
                except:
                    print("Invalid input!")

            while True:
                input_episode = input("Number of Episodes (default=50): ")

                if input_episode.lower() == "q":
                    print("Quitting!")
                    sys.exit(0)

                elif input_episode == "":
                    booleansSimulation.append(50)
                    break

                try:
                    episodes = int(input_episode)

                    if episodes > 0:
                        booleansSimulation.append(episodes)
                        break
                    else:
                        raise Exception
                except:
                    print("Invalid input!")

            while True:
                input_runs = input("Number of Runs (default=10): ")

                if input_runs.lower() == "q":
                    print("Quitting!")
                    sys.exit(0)

                elif input_runs == "":
                    booleansSimulation.append(10)
                    break

                try:
                    runs = int(input_runs)

                    if runs > 0:
                        booleansSimulation.append(runs)
                        break
                    else:
                        raise Exception
                except:
                    print("Invalid input!")

            while True:
                input_goal = input("Set goal reward (default=0): ")

                if input_goal.lower() == "q":
                    print("Quitting!")
                    sys.exit(0)

                elif input_goal == "":
                    booleansSimulation.append(0)
                    break

                try:
                    goal = int(input_goal)
                    booleansSimulation.append(goal)
                    break
                except:
                    print("Invalid input!")
            

        print("Output\n"
              "------")
            
        booleansOutput = []

        for string in ["Sum of rewards chart (y/n): ", "Visited states heatmap (y/n): "]:
            booleansOutput.append(self.boolean_check(string))

        return board_size, window_size, booleansSearch, booleansSimulation, booleansOutput

    def float_check(self,input_string):
        
        while True:
            input_float = input(input_string)

            if input_float == "q" or input_float == "Q":
                print("Quitting!")
                sys.exit(0)
            
            try:
                float_value = float(input_float)
                if float_value >= 0.0 and float_value <= 1.0:
                    return float_value
                else:
                    raise Exception

            except:
                print("Invalid input!")

    def input_check(self,input_string):

        while True:
            input_int = input(input_string)

            if input_int == "q" or input_int == "Q":
                print("Quitting!")
                sys.exit(0)

            try:
                int_value = int(input_int)

                if int_value > 0:
                    return int_value
                else:
                    raise Exception
            except:
                print("Invalid input!")


    def boolean_check(self, input_string):

        while True:
            input_bool = input(input_string)

            if input_bool == "q" or input_bool == "Q":
                print("Quitting!")
                sys.exit(0)
            elif input_bool == "y" or input_bool == "Y":
                return True
            elif input_bool == "n" or input_bool == "N":
                return False