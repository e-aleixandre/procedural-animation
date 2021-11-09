import gym
import numpy as np
import matplotlib.pyplot as plt
import argparse

"""
    Declarations
"""
alpha = 0.1
gamma = 0.95
environment = "FrozenLake-v0"
episodes = 5000
steps = 100

"""
    Argument definition
"""
parser = argparse.ArgumentParser()
parser.add_argument("--alpha", "-a")
parser.add_argument("--gamma", "-g")
parser.add_argument("--episodes", "-e")
parser.add_argument("--steps", "-s")
parser.add_argument("environment")

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
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < 99:
        j += 1

        a = np.argmax(Q[s, :] + np.random.randn(1, env.action_space.n) * (1. / (i + 1)))

        s1, r, d, _ = env.step(a)

        Q[s, a] = Q[s, a] + alpha * (r + gamma * np.max(Q[s1, :]) - Q[s, a])
        rAll += r
        s = s1
        if d:
            break

        rev_list.append(rAll)

np.savetxt("Q_table.txt", Q)

plt.plot(rev_list)
plt.show()

env.close()
