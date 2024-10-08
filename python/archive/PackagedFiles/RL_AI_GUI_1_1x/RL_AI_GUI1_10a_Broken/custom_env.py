import gymnasium as gym
import numpy as np
import pandas as pd
from gymnasium import spaces

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
        self.best_balance = self.balance  # Track the best balance
        self.best_iteration = self.current_step  # Track the best iteration

        # Define action and observation space
        # Action space: 0: hold, 1: buy, 2: sell
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(data.shape[1],), dtype=np.float32)

    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data):
            terminated = True
            truncated = False
            reward = 0
            obs = np.zeros(self.observation_space.shape)  # Return a zero observation
        else:
            terminated = False
            truncated = False
            reward = self._calculate_reward(action)
            self.cumulative_reward += reward  # Update cumulative reward
            obs = self.data.iloc[self.current_step].values

            # Track the best balance and iteration
            if self.balance > self.best_balance:
                self.best_balance = self.balance
                self.best_iteration = self.current_step

        info = {
            'balance': self.balance,
            'cumulative_reward': self.cumulative_reward
        }

        return obs, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = 1000  # Reset balance
        self.position = None  # Reset position
        self.entry_price = 0  # Reset entry price
        self.cumulative_reward = 0  # Reset cumulative reward
        self.best_balance = self.balance  # Reset best balance
        self.best_iteration = self.current_step  # Reset best iteration
        return self.data.iloc[self.current_step].values, {'balance': self.balance}

    def render(self, mode='human'):
        if self.render_mode == 'human':
            # Implement rendering logic
            print(f"Step: {self.current_step}, Balance: {self.balance}")

    def _calculate_reward(self, action):
        current_price = self.data.iloc[self.current_step]['close']
        next_price = self.data.iloc[self.current_step + 1]['open'] if self.current_step + 1 < len(self.data) else current_price

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

    def get_best_iteration_details(self):
        return self.best_iteration, self.best_balance