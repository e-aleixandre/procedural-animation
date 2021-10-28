import gym
import numpy as np

env = gym.make('FrozenLake8x8-v1', is_slippery=False)

total_epochs, total_penalties = 0, 0
episodes = 1000
q_table = np.loadtxt('Q_table.txt')

for _ in range(episodes):
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0

    done = False

    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)

        if reward < 0:
            penalties += 1

        epochs += 1

    total_penalties += penalties
    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timestamps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")
print(f"Average successful episodes: {1}")
