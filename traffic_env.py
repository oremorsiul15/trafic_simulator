import gym
from gym import spaces
from traffic import Game
import numpy as np
import pygame


class TrafficSimEnv(gym.Env):
    def __init__(self):
        super(TrafficSimEnv, self).__init__()
        self.game = Game()
        self.game.init()
        self.game.load_project('project.pickle')

        # Assuming each stoplight can be either 0 or 1
        # self.action_space = spaces.MultiBinary(len(self.game.stoplights))
        self.action_space = spaces.Discrete(2 ** len(self.game.stoplights))

        # For observation space, this is an example assuming each stoplight state can be 0 or 1,
        # each path can overflow or not, and there is a collision or not
        # self.observation_space = spaces.Box(
        #     low=0, high=2, shape=(17,), dtype=np.int32)
        self.observation_space = spaces.Box(
            low=0, high=2, shape=(21617,), dtype=np.int32)

    def step(self, action):
        # Execute action
        self.game.action(action)

        # Update the game state
        self.game.update()

        # Get observation
        observation = self.game.get_observation()

        # Define reward
        reward = self.calculate_reward(observation)

        # Define if the episode is done
        done = self.is_done(observation)

        return observation, reward, done, {}

    def reset(self):
        self.game.init()
        self.game.load_project('project.pickle')
        return self.game.get_observation()

    def render(self, mode='human'):
        if mode == 'human':
            self.game.draw()
            # pygame.display.flip()
        elif mode == 'rgb_array':
            data = pygame.surfarray.array3d(self.game.map)
            # transpose to make it (height, width, channel)
            return np.transpose(data, axes=[1, 0, 2])
        else:
            # just call the default implementation, which will raise an error
            super().render(mode=mode)

    def calculate_reward(self, observation):
        # Implement your reward calculation logic
        # This is just a placeholder
        # print(list[bool](observation[8:15]),
        #       len(list[bool](observation[8:16])))
        return -1 if bool(observation[16]) or any(list[bool](observation[8:16])) else 0.1

    def is_done(self, observation):
        # Implement your logic to determine when the episode is done
        # This is just a placeholder
        return bool(observation[16]) or any(list[bool](observation[8:16]))

    def close(self):
        if self.game:
            self.game.close()
            self.game = None
