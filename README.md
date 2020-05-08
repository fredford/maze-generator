# Q-Learning and Expected Sarsa





# Testing

## Agents

Testing the methods associated to the Q-Learning and Expected Sarsa agents includes the following functionality:


`agent_start(self, state)`
* The initialization of the first state-action pair that the agent will use, taking the current state as an argument

`agent_step(self, reward, state)`
* The process where the agent selects an action given it's current state and updates it's action-value estimate with this data, taking the current state and the reward from the previous state-action pair as arguments

`agent_end(self, reward)`
* The last action-value estimate update with the current state-action pair being absent, taking the reward received in the previous state-action pair as an argument 

The following unit testing runs through a sample case demostrating the expected estimates produced as well as the actions selected:

```
$ python3 -m unittest test.test_q_learning
$ python3 -m unittest test.test_e_sarsa
```
 
 ## Environment

Testing the agents in an established environment of the commonly used _Cliff World_. 

 <p align="center">
    <img src="cliffworld.png" width="600"/>
</p>