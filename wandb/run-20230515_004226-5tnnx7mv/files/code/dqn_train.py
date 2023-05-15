import os
import gym
import numpy as np
import wandb
from wandb.integration.sb3 import WandbCallback

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.utils import set_random_seed

from CustomPolicy import CustomPolicy

from traffic_env import TrafficSimEnv

config = {
    "policy_type": 'MlpPolicy',
    "total_timesteps": 2_000_000,
    "learning_rate": 0.0003,
    "env_name": "Traffic UPRM",
}
run = wandb.init(
    project="DQN Traffic Simulation RL",
    config=config,
    sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
    monitor_gym=True,  # auto-upload the videos of agents playing the game
    save_code=True,  # optional
)


def make_env(rank, seed=0):
    def _init():
        env = TrafficSimEnv()
        env.seed(seed + rank)
        return env

    set_random_seed(seed)
    return _init


if __name__ == '__main__':
    log_dir = "tmp/"

    num_cpu = 1

    env = VecMonitor(DummyVecEnv([make_env(i)
                                  for i in range(num_cpu)]), "tmp/monitor")

    model = DQN(config["policy_type"], env, verbose=1,
                tensorboard_log=f"runs/{run.id}", buffer_size=100)
    model.learn(
        total_timesteps=config["total_timesteps"],
        callback=WandbCallback(
            gradient_save_freq=300,
            model_save_path="models/DQN",
            verbose=2,
        ),
    )
    run.finish()
