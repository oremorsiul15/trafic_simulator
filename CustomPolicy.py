import gym
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import torch.nn as nn
import torch


class CustomFeatureExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Space):
        super(CustomFeatureExtractor, self).__init__(
            observation_space, features_dim=64)

        self.network = nn.Sequential(
            nn.Linear(observation_space.shape[0], 64),
            nn.ReLU(),
            nn.Linear(64, 124),
            nn.ReLU(),
            nn.Linear(124, 124),
            nn.ReLU(),
            nn.Linear(124, 64),
            nn.ReLU(),
        )

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.network(observations)


class CustomPolicy(ActorCriticPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           features_extractor_class=CustomFeatureExtractor)