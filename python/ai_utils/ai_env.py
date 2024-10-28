import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TradingEnv(gym.Env):
    def __init__(self, data, symbol, timeframe):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)  # Shape should be (7,)
        self.symbol = symbol
        self.timeframe = timeframe
        self.buy_price = None  # Initialize buy_price here
        
    def reset(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.current_step = 0
        
        # Access data using integer indexing
        obs = self.data[self.current_step, 1:8]  # Assuming 'open', 'high', 'low', 'close', 'tick_volume', 'hour_of_day', 'day_of_week' are columns 1 to 7

        return obs, {}

    def step(self, action):
        self.current_step += 1
        reward = self._calculate_reward(action)
        done = self.current_step >= len(self.data) - 1

        if not done:
            # Access data using integer indexing
            obs = self.data[self.current_step, 1:8]  # Assuming 'open', 'high', 'low', 'close', 'tick_volume', 'hour_of_day', 'day_of_week' are columns 1 to 7
        else:
            obs = np.zeros(self.observation_space.shape)

        truncated = False
        return obs, reward, done, truncated, {}

    def _calculate_reward(self, action):
        if action == 0:  # Buy
            self.buy_price = self.data[self.current_step, 4]  # Assuming 'close' is the fifth column
            return 0  # No immediate reward for buying (cast to int)
        elif action == 1:  # Sell
            if self.buy_price is not None:
                profit = self.data[self.current_step, 4] - self.buy_price  # Assuming 'close' is the fifth column
                self.buy_price = None  # Reset buy price
                if profit > 0:
                    return float(profit * 1.1)  # Reward for profit (cast to float)
                else:
                    return float(profit)  # Return the loss as the reward (cast to float)
            else:
                return int(-1)  # Penalty for selling without a position (cast to int)
        else:  # Hold
            return int(0)  # No reward for holding (cast to int)