import os
import gym
from stable_baselines3 import A2C
from traffic_env import TrafficSimEnv

model_dir = "model"
model = A2C.load("./models/A2C/model.zip")


def test_agent(model, env, max_steps=6000):
    obs = env.reset()
    for _ in range(max_steps):
        action, _ = model.predict(obs)
        obs, _, done, _ = env.step(action)
        env.render()
        if done:
            break


env = TrafficSimEnv()
for i in range(10):
    test_agent(model, env)
env.close()
