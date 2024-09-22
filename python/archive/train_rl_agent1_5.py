import warnings
warnings.filterwarnings("ignore", message="You tried to call render() but no `render_mode` was passed to the env constructor.")

import tkinter as tk
from tkinter import messagebox
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from custom_env import CustomEnv, load_prepared_data
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def evaluate_model(model, env, num_episodes=10):
    all_rewards = []
    total_profit_percentage = 0
    initial_balance = env.unwrapped.get_attr('balance')[0]  # Get the initial balance at the start of evaluation

    for episode in range(num_episodes):
        obs = env.reset()
        episode_rewards = 0
        done = False
        iteration = 0  # Initialize iteration counter
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, infos = env.step(action)
            episode_rewards += rewards
            iteration += 1  # Increment iteration counter

            # Print iteration details
            print(f"Iteration: {iteration}, Action: {action}, Reward: {rewards}, Balance: {env.unwrapped.get_attr('balance')[0]}")

        all_rewards.append(episode_rewards)
        final_balance = env.unwrapped.get_attr('balance')[0]
        profit_percentage = ((final_balance - initial_balance) / initial_balance) * 100
        total_profit_percentage += profit_percentage

    avg_reward = sum(all_rewards) / num_episodes
    avg_profit_percentage = total_profit_percentage / num_episodes

    print(f"Average Reward over {num_episodes} episodes: {avg_reward}")
    print(f"Average Profit Percentage over {num_episodes} episodes: {avg_profit_percentage}%")
    print(f"Final Balance: {final_balance}")
    print(f"Initial Balance: {initial_balance}")

    # Define thresholds
    reward_threshold = 50  # Example threshold for average reward
    profit_percentage_threshold = 10  # Example threshold for average profit percentage (10%)

    # Provide feedback based on thresholds and final balance
    if avg_reward >= reward_threshold and avg_profit_percentage >= profit_percentage_threshold and final_balance >= initial_balance and avg_profit_percentage >= 0:
        print("The model's performance is good.")
    else:
        print("The model's performance is not satisfactory.")

def main():
    print("Starting training...")
    file_path = './data/processed/MarketData_Prepared.tsv'
    data = load_prepared_data(file_path)  # Ensure data is loaded here
    print("Successfully loaded prepared data.")
    print(f"Column names in the dataset: {data.columns}")

    target_column = 'Close'
    features = data.drop(columns=[target_column])
    target = data[target_column]

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(features, target)
    feature_importance = pd.Series(rf.feature_importances_, index=features.columns).sort_values(ascending=False)
    top_features = feature_importance.head(9).index.tolist()
    if 'Close' not in top_features:
        top_features.append('Close')
    selected_data = data[top_features]

    env = DummyVecEnv([lambda: Monitor(CustomEnv(selected_data))])
    model = PPO('MlpPolicy', env, verbose=1, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    eval_env = DummyVecEnv([lambda: Monitor(CustomEnv(selected_data))])
    eval_callback = EvalCallback(eval_env, best_model_save_path='./logs/best_model', log_path='./logs/', eval_freq=5000, deterministic=True, render=False)
    new_logger = configure('./logs/', ["stdout", "tensorboard"])
    model.set_logger(new_logger)
    model.learn(total_timesteps=20000, callback=eval_callback)

    evaluate_model(model, env)

if __name__ == "__main__":
    main()