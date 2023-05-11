import os
import gym
import numpy as np
import wandb
from wandb.integration.sb3 import WandbCallback

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecVideoRecorder
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import BaseCallback

from CustomPolicy import CustomPolicy

from traffic_env import TrafficSimEnv

config = {
    "policy_type": "CustomPolicy",
    "total_timesteps": 20_000_000,
    "learning_rate": 0.0003,
    "env_name": "CartPole-v1",
}
run = wandb.init(
    project="Traffic Simulation RL",
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

    num_cpu = 12

    env = VecMonitor(SubprocVecEnv([make_env(i)
                                    for i in range(num_cpu)]), "tmp/monitor")

    # model = PPO(CustomPolicy, env, verbose=1)

    # print('------------ Starting Learning -----------------')
    # model.learn(total_timesteps=config["total_timesteps"],
    #             callback=WandbCallback(), tb_log_name="PPO-00003")
    # model.save('spaceship_game_dqn')
    # print('------------ Done Learning -----------------')
    # env = DummyVecEnv([make_env])
    env = VecVideoRecorder(
        env, f"videos/{run.id}", record_video_trigger=lambda x: x % 2000 == 0, video_length=200)
    model = PPO(config["policy_type"], env, verbose=1,
                tensorboard_log=f"runs/{run.id}")
    model.learn(
        total_timesteps=config["total_timesteps"],
        callback=WandbCallback(
            gradient_save_freq=100,
            model_save_path=f"models/{run.id}",
            verbose=2,
        ),
    )
    run.finish()
