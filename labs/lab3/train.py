import gym
import numpy as np

env = gym.make('FrozenLake8x8-v1', is_slippery=False)

Q = np.zeros([env.observation_space.n, env.action_space.n])

alpha = 0.9
gamma = 0.9
episodes = 5000
rev_list = []

for i in range(episodes):
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < 99:
        j += 1

        a = np.argmax(Q[s,:] + np.random.randn(1, env.action_space.n) * (1. / (i + 1)))
        
        s1, r, d, _ = env.step(a)

        Q[s, a] = Q[s, a] + alpha * (r + gamma * np.max(Q[s1, :]) - Q[s, a])
        rAll += r
        s = s1
        if d == True:
            break

        rev_list.append(rAll)
        
np.savetxt("Q_table.txt", Q)

env.close()