import os
import json
from ai_utils.ai_env import TradingEnv
from ai_utils.normalize_data import normalize_data
from rl_algorithms.functions import initialize_algorithms, rl_algorithms
from appdirs import user_data_dir
import pandas as pd
import re

def main():
    # 1. Load Settings (only for algorithm selection)
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
    settings_file = os.path.join(user_data_path, 'settings', 'algorithm_settings.json')
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    selected_algorithm = settings['selected_algorithm'].upper()

    # 2. Prepare Data
    normalized_data_dir = os.path.join(user_data_path, 'forex_data', 'normalized')

    # Find the normalized data file
    for filename in os.listdir(normalized_data_dir):
        if filename.endswith("_normalized.csv"):
            normalized_data_file = os.path.join(normalized_data_dir, filename)
            break
    else:
        raise FileNotFoundError("No normalized data file found.")

    # Extract symbol and timeframe from filename
    match = re.match(r"(.+)_(\w+)_normalized\.csv", filename)
    if match:
        symbol, timeframe = match.groups()
    else:
        raise ValueError(f"Could not extract symbol and timeframe from filename: {filename}")

    # Load the normalized data into a DataFrame
    normalized_data = pd.read_csv(normalized_data_file)

    # 3. Create Trading Environment
    env = TradingEnv(normalized_data, symbol, timeframe)

    # 4. Initialize RL Algorithm
    initialize_algorithms()
    algorithm_func = rl_algorithms.get(selected_algorithm)
    if algorithm_func is None:
        raise ValueError(f"Invalid algorithm selected: {selected_algorithm}")

    # 5. Create RL Agent Instance
    algorithm_params = settings.get(selected_algorithm, {}).get('params', {})
    total_timesteps = int(algorithm_params.pop('total_timesteps', 1000))
    algorithm_params.pop('module_path', None)  # Remove module_path if it exists
    algorithm_params['learning_rate'] = float(algorithm_params.get('learning_rate', 0.0007))
    algorithm_params['n_steps'] = int(algorithm_params.get('n_steps', 5))

    # 'buffer_size' is not a parameter for A2C, PPO, etc. in Stable Baselines3
    # It's handled internally by the algorithms.
    # Remove it from algorithm_params
    algorithm_params.pop('buffer_size', None)  

    agent = algorithm_func(env, **algorithm_params)

    # 6. Train RL Agent
    for timestep in range(1, total_timesteps + 1):
        agent.learn(total_timesteps=1)
        if timestep % 100 == 0:
            print(f"Training progress: {timestep}/{total_timesteps} timesteps")

    # 7. (Optional) Evaluate and Save Agent
    # ... (add code to evaluate the trained agent, e.g., on a test dataset)
    # ... (save the trained agent if needed)

if __name__ == "__main__":
    main()
