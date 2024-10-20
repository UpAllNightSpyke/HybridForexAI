import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TradingEnv(gym.Env):
    def __init__(self, data, symbol, timeframe):  # Add symbol and timeframe arguments
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = spaces.Discrete(4)  # 0: Buy, 1: Sell, 2: Hold Short Term, 3: Hold Long Term
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(data.shape[1],), dtype=np.float32)
        self.symbol = symbol
        self.timeframe = timeframe
        
    def reset(self):
        self.current_step = 0
        return self.data[self.current_step]

    def step(self, action):
        self.current_step += 1
        reward = self._calculate_reward(action)
        done = self.current_step >= len(self.data) - 1
        obs = self.data[self.current_step] if not done else np.zeros(self.data.shape[1])
        return obs, reward, done, {}

    def _calculate_reward(self, action):
        if action == 0:  # Buy
            self.buy_price = self.data['close'][self.current_step]
            return 0  # No immediate reward for buying
        elif action == 1:  # Sell
            if self.buy_price is not None:
                profit = self.data['close'][self.current_step] - self.buy_price
                self.buy_price = None  # Reset buy price
                if profit > 0:
                    return profit * 1.1  # Reward for profit (10% bonus)
                else:
                    return profit  # Return the loss as the reward
            else:
                return -1  # Penalty for selling without a position
        else:  # Hold
            return 0  # No reward for holding