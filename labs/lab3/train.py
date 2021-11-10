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
environment = "FrozenLake-v0"
episodes = 5000
steps = 100

"""
    Argument definition
"""
parser = argparse.ArgumentParser()
parser.add_argument("--alpha", "-a", help="Learning rate, default: 0.1")
parser.add_argument("--gamma", "-g", help="Discount factor, default: 0.95")
parser.add_argument("--episodes", "-e", help="Number of episodes, default: 5000")
parser.add_argument("--steps", "-s", help="Steps per episode, default: 100")
parser.add_argument("environment", help="OpenAI environment, default: OpenLake-v1")

"""
    Argument parsing
"""
args = parser.parse_args()

alpha = alpha if args.alpha is None else float(args.alpha)
gamma = gamma if args.gamma is None else float(args.gamma)
environment = environment if args.environment is None else args.environment
episodes = episodes if args.episodes is None else int(args.episodes)
steps = steps if args.steps is None else int(args.steps)

"""
    Initialization
"""
env = gym.make(environment, is_slippery=False)

Q = np.zeros([env.observation_space.n, env.action_space.n])

rev_list = []

"""
    Q-Learning
"""

for i in range(episodes):
    state = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < 99:
        j += 1

        action = np.argmax(Q[state, :] + np.random.randn(1, env.action_space.n) * (1. / (i + 1)))

        new_state, reward, d, _ = env.step(action)

        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[new_state, :]) - Q[state, action])
        rAll += reward
        state = new_state

        if d:
            break

        rev_list.append(rAll)

np.savetxt("Q_table.txt", Q)
plt.plot(rev_list)
plt.show()

env.close()
