import gym
import numpy as np
import pandas as pd
from gym import spaces

class CustomEnv(gym.Env):
    def __init__(self, data, render_mode=None):
        super(CustomEnv, self).__init__()
        self.data = data
        self.render_mode = render_mode
        # Define action and observation space
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=1, shape=(data.shape[1],), dtype=np.float32)

    def step(self, action):
        # Implement step logic
        pass
    
    def reset(self):
        self.current_step = 0
        return self.data.iloc[self.current_step].values

    def render(self, mode='human'):
        if self.render_mode == 'human':
            # Implement rendering logic
            pass
        
    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data):
            done = True
            reward = 0
            obs = np.zeros(self.observation_space.shape)  # Return a zero observation
        else:
            done = False
            reward = self._calculate_reward(action)
            obs = self.data.iloc[self.current_step].values
        return obs, reward, done, {}
    
    def _calculate_reward(self, action):
        # Implement reward calculation logic
        # Ensure reward is not NaN
        reward = 1  # Placeholder reward
        if np.isnan(reward):
            reward = 0
        return reward
    
    def render(self, mode='human'):
        pass

def load_prepared_data(file_path):
    # Open the file in binary read mode
    with open(file_path, 'rb') as file:
        raw_data = file.read()  # Read the entire file content into raw_data
        # Determine the file encoding based on the byte order mark (BOM)
        if raw_data.startswith(b'\xef\xbb\xbf'):
            encoding = 'utf-8-sig'  # UTF-8 with BOM
        elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
            encoding = 'utf-16'  # UTF-16
        else:
            encoding = 'latin1'  # Default to Latin-1 encoding

    # Read the file with the determined encoding
    data = pd.read_csv(file_path, delimiter='\t', encoding=encoding)
    print("Successfully loaded prepared data.")
    return data