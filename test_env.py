import gym
from traffic_env import TrafficSimEnv

env = TrafficSimEnv()
observation = env.reset()

for _ in range(1000):
    env.render()
    action = env.action_space.sample()  # take a random action
    # print(action)
    observation, reward, done, info = env.step(action)
    print(len(observation))
    if done:
        observation = env.reset()

env.close()
