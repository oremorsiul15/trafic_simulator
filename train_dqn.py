import os
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from traffic_env import TrafficSimEnv


def make_env():
    env = TrafficSimEnv()
    env = Monitor(env)
    return env


# Set the hyperparameters
total_timesteps = 1_000_000
learning_rate = 0.0005
buffer_size = 100000
exploration_fraction = 0.1
exploration_final_eps = 0.05
train_freq = 10
target_update_interval = 1000

# Create the environment
env = DummyVecEnv([make_env])

model = DQN(
    "MlpPolicy",
    env,
    learning_rate=learning_rate,
    buffer_size=buffer_size,
    exploration_fraction=exploration_fraction,
    exploration_final_eps=exploration_final_eps,
    train_freq=train_freq,
    target_update_interval=target_update_interval,
    verbose=1,
)

model.learn(total_timesteps=total_timesteps)

mean_reward, std_reward = evaluate_policy(
    model, env, n_eval_episodes=10, render=True)
print(f"Mean reward: {mean_reward}, Std reward: {std_reward}")

model_dir = "model"
os.makedirs(model_dir, exist_ok=True)
model.save(os.path.join(model_dir, "traffic_dqn"))
