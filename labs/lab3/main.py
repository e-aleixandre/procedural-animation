import gym
import numpy as np
import matplotlib.pyplot as plt
import argparse

"""
    Function declaration
"""


def pick_action(state, exploration_threshold):
    if exploration_threshold > exploration_rate:
        return np.argmax(Q[state, :])
    else:
        return env.action_space.sample()


def train_agent():
    global exploration_rate
    rev_list = []
    rewards = 0

    for i in range(episodes):
        state = env.reset()
        done = False
        action = None

        for j in range(steps):
            """
                Decide between exploration and exploitation
            """
            exploration_threshold = np.random.random()

            action = pick_action(state, exploration_threshold)

            """
                Perform the action, get results
            """
            new_state, reward, done, _ = env.step(action)

            if render:
                env.render()

            # Sarsa table updating
            if sarsa:
                new_action = pick_action(new_state, exploration_threshold)

                Q[state, action] = \
                    Q[state, action] + alpha * (reward + gamma * Q[new_state, new_action] - Q[state, action])

                action = new_action
            # Q-Learning table updating
            else:
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

    return rev_list


def test_agent():
    total_steps = []
    total_succeeded = []
    succeeded = 0

    for _ in range(episodes):
        state = env.reset()
        steps = 0
        done = False

        while not done:
            action = np.argmax(Q[state])
            state, reward, done, info = env.step(action)

            if render:
                env.render()
            if reward > 0:
                succeeded += 1

            steps += 1

        total_succeeded.append(succeeded)
        total_steps.append(steps)

    return total_succeeded, total_steps


"""
    Declarations
"""
# Learning rate
alpha = 0.1

# Discount factor
gamma = 0.95

environment = "FrozenLake-v1"
episodes = 500
steps = 50
sarsa = False

# Epsilon greedy strategy
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_rate = max_exploration_rate
exploration_decay_rate = 0.001

filename = "Q_table"
test = False
render = False

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
parser.add_argument("--decay-rate", "-d", help="Exploration decay rate, default: 0.001", type=float)
parser.add_argument("--output", "-o", help="Q-table output file, default: Q_table", type=str)
parser.add_argument("--test", "-t", action="store_true", help="Test a Q-table with an environment")
parser.add_argument("--input", "-i", help="Q-table input file, default: Q_table", type=str)
parser.add_argument("--render", "-r", action="store_true", help="Render each step")

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
sarsa = args.sarsa
test = args.test
render = args.render

if test:
    filename = filename if args.input is None else args.input
else:
    filename = filename if args.output is None else args.output

"""
    Initialization
"""
env = gym.make(environment, is_slippery=True)

if test:
    Q = np.loadtxt("%s.txt" % filename)
else:
    Q = np.zeros([env.observation_space.n, env.action_space.n])

"""
    Algorithm
"""

if test:
    total_succeeded, total_steps = test_agent()

    """
        Plot the results
    """
    plt.xlabel("Episodes")
    plt.ylabel("Succeeded")
    plt.plot(total_succeeded)
    plt.show()

    plt.xlabel("Episodes")
    plt.ylabel("Steps")
    plt.plot(total_steps)
    plt.show()
else:
    rev_list = train_agent()

    """
        Export Q table to test the agent elsewhere
    """
    np.savetxt("%s.txt" % filename, Q)

    """
        Plot the results
    """
    plt.xlabel("Episodes")
    plt.ylabel("Rewards")
    plt.plot(rev_list)
    plt.show()

env.close()
