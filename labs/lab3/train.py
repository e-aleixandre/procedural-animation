import gym
import numpy as np
import matplotlib.pyplot as plt
import argparse

"""
    Declarations
"""
# Learning rate
alpha = 0.1

# Discount factor
gamma = 0.95

environment = "FrozenLake-v1"
episodes = 5000
steps = 100
sarsa = False

# Epsilon greedy strategy
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_rate = max_exploration_rate
exploration_decay_rate = 0.001

"""
    Argument definition
"""
parser = argparse.ArgumentParser()
parser.add_argument("--sarsa", action="store_true", help="Change from Q-Learning to Sarsa")
parser.add_argument("--alpha", "-a", help="Learning rate, default: 0.1", type=float)
parser.add_argument("--gamma", "-g", help="Discount factor, default: 0.95", type=float)
parser.add_argument("--episodes", "-e", help="Number of episodes, default: 5000", type=int)
parser.add_argument("--steps", "-s", help="Steps per episode, default: 100", type=int)
parser.add_argument("environment", help="OpenAI environment to load", type=str)
parser.add_argument("--decay-rate", "-o", help="Exploration decay rate, default: 0.001", type=float)

"""
    Argument parsing
"""
args = parser.parse_args()
alpha = alpha if args.alpha is None else args.alpha
gamma = gamma if args.gamma is None else args.gamma
environment = environment if args.environment is None else args.environment
episodes = episodes if args.episodes is None else args.episodes
steps = steps if args.steps is None else args.steps
exploration_decay_rate = exploration_decay_rate if args.decay_rate is None else args.decay_rate

"""
    Initialization
"""
env = gym.make(environment, is_slippery=False)

Q = np.zeros([env.observation_space.n, env.action_space.n])

rev_list = []

"""
    Q-Learning
"""
rewards = 0

for i in range(episodes):
    state = env.reset()
    done = False

    for j in range(steps):
        """
            Decide between exploration and exploitation
        """
        exploration_threshold = np.random.random()

        if exploration_threshold > exploration_rate:
            action = np.argmax(Q[state, :])
        else:
            action = env.action_space.sample()

        """
            Perform the action, get results
        """
        new_state, reward, done, _ = env.step(action)

        Q[state, action] = \
            (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[new_state, :]))
        rewards += reward
        state = new_state

        """
            End the current episode if environment is over
        """
        if done:
            break

    """
        After each episode, decrease the exploration rate to move towards exploitation
    """
    exploration_rate = \
        min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * i)

    """
        And add the episode rewards to the list of rewards
    """
    rev_list.append(rewards)

"""
    Export Q table to test the agent elsewhere
"""
np.savetxt("Q_table.txt", Q)

"""
    Plot the results
"""

plt.plot(rev_list)
plt.show()

env.close()
