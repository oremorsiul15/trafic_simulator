import os
import gym
from stable_baselines3 import PPO
from traffic_env import TrafficSimEnv

model_dir = "model"
model = PPO.load("./models/mqlq25wx/model.zip")


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
