import gym
import numpy as np
import pandas as pd
from gym import spaces

class CustomEnv(gym.Env):
    def __init__(self, data, render_mode=None):
        super(CustomEnv, self).__init__()
        self.data = data
        self.render_mode = render_mode
        self.current_step = 0
        self.balance = 1000  # Initial balance
        self.position = None  # Current position: None, 'buy', or 'sell'
        self.entry_price = 0  # Price at which the position was entered
        self.transaction_costs = 0.10  # Example transaction cost
        self.cumulative_reward = 0  # Initialize cumulative reward
        self.risk_percentage = 0.05  # Risk percentage (5%)

        # Define action and observation space
        # Action space: 0: hold, 1: buy, 2: sell
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(data.shape[1],), dtype=np.float32)

    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data):
            done = True
            reward = 0
            obs = np.zeros(self.observation_space.shape)  # Return a zero observation
        else:
            done = False
            reward = self._calculate_reward(action)
            self.cumulative_reward += reward  # Update cumulative reward
            obs = self.data.iloc[self.current_step].values

        info = {}

        return obs, reward, done, info

    def reset(self):
        self.current_step = 0
        self.balance = 1000  # Reset balance
        self.position = None  # Reset position
        self.entry_price = 0  # Reset entry price
        self.cumulative_reward = 0  # Reset cumulative reward
        return self.data.iloc[self.current_step].values

    def render(self, mode='human'):
        if self.render_mode == 'human':
            # Implement rendering logic
            print(f"Step: {self.current_step}, Balance: {self.balance}")

    def _calculate_reward(self, action):
        current_price = self.data.iloc[self.current_step]['Close']
        next_price = self.data.iloc[self.current_step + 1]['Open'] if self.current_step + 1 < len(self.data) else current_price

        previous_balance = self.balance
        risk_amount = self.balance * self.risk_percentage
        lot_size = risk_amount / current_price

        if action == 1:  # Buy
            if self.position is None:
                self.position = 'buy'
                self.entry_price = current_price
                reward = 0
            else:
                reward = 0
        elif action == 2:  # Sell
            if self.position is None:
                self.position = 'sell'
                self.entry_price = current_price
                reward = 0
            else:
                reward = 0
        else:  # Hold
            reward = 0

        if self.position == 'buy' and action == 2:
            profit = (next_price - self.entry_price - self.transaction_costs) * lot_size
            self.balance += profit
            reward = self.balance - previous_balance
            self.position = None
        elif self.position == 'sell' and action == 1:
            profit = (self.entry_price - next_price - self.transaction_costs) * lot_size
            self.balance += profit
            reward = self.balance - previous_balance
            self.position = None

        # Additional reward for maintaining a positive balance
        if self.balance > previous_balance:
            reward += 0.1 * (self.balance - previous_balance)

        if np.isnan(reward):
            reward = 0
        return reward

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