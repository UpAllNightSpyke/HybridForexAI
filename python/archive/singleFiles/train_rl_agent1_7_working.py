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
from python.archive.custom_env1_6_working import CustomEnv
from python.archive.preprocess1_0_working import preprocess_observation, preprocess_action, load_prepared_data, select_top_features

def evaluate_model(model, env, num_episodes=10):
    all_rewards = []
    total_profit_percentage = 0
    best_iteration = 0
    best_balance = float('-inf')
    best_mean_reward = float('-inf')  # Initialize best mean reward to negative infinity

    for episode in range(num_episodes):
        obs = env.reset()
        obs = obs[0]  # Extract the first element from the list
        initial_balance = 1000  # Assuming initial balance is 1000
        episode_rewards = 0
        done = False
        iteration = 0  # Initialize iteration counter
        while not done:
            obs = preprocess_observation(obs)  # Preprocess observation
            action, _states = model.predict(obs)
            action = preprocess_action(action)  # Preprocess action
            obs, rewards, dones, infos = env.step([action])  # Pass action as a list
            obs = obs[0]  # Extract the first element from the list
            rewards = rewards[0]  # Extract the first element from the list
            dones = dones[0]  # Extract the first element from the list
            infos = infos[0]  # Extract the first element from the list
            episode_rewards += rewards
            iteration += 1  # Increment iteration counter

            current_balance = infos['balance']
            # Print iteration details
            print(f"Iteration: {iteration}, Action: {action}, Reward: {rewards}, Balance: {current_balance}")

            # Track the best iteration and balance
            if current_balance > best_balance:
                best_iteration = iteration
                best_balance = current_balance

            done = dones  # Update done status

        all_rewards.append(episode_rewards)
        profit_percentage = ((best_balance - initial_balance) / initial_balance) * 100
        total_profit_percentage += profit_percentage

    avg_reward = sum(all_rewards) / num_episodes
    avg_profit_percentage = total_profit_percentage / num_episodes

    print(f"Average Reward over {num_episodes} episodes: {avg_reward}")
    print(f"Average Profit Percentage over {num_episodes} episodes: {avg_profit_percentage}%")
    print(f"Initial Balance: {initial_balance}")

    # Define thresholds
    reward_threshold = 50  # Example threshold for average reward
    profit_percentage_threshold = 10  # Example threshold for average profit percentage (10%)

    # Provide feedback based on best balance and best iteration
    if best_balance >= initial_balance and avg_profit_percentage >= profit_percentage_threshold:
        print("The model's performance is good.")
    else:
        print("The model's performance is not satisfactory.")

    # Print best iteration details
    print(f"Best Iteration: {best_iteration}, Best Balance: {best_balance}")

    # Check if a new best mean reward is found
    if avg_reward > best_mean_reward:
        best_mean_reward = avg_reward
        print("New best mean found!")

def main():
    print("Starting training...")
    file_path = './data/processed/MarketData_Prepared.tsv'
    data = load_prepared_data(file_path)  # Ensure data is loaded here
    print("Successfully loaded prepared data.")
    print(f"Column names in the dataset: {data.columns}")

    selected_data = select_top_features(data)

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