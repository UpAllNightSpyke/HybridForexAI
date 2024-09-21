import warnings
warnings.filterwarnings("ignore", message="You tried to call render() but no `render_mode` was passed to the env constructor.")

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
    correct_actions = 0
    total_actions = 0
    total_profit = 0

    for episode in range(num_episodes):
        obs = env.reset()
        episode_rewards = 0
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, infos = env.step(action)
            episode_rewards += rewards

            info = infos[0] if isinstance(infos, list) else infos
            if 'correct_action' in info:
                correct_actions += (action == info['correct_action'])
            total_actions += 1

        all_rewards.append(episode_rewards)
        total_profit += env.get_attr('balance')[0] - 1000  # Assuming initial balance is 1000

    avg_reward = sum(all_rewards) / num_episodes
    accuracy = correct_actions / total_actions if total_actions > 0 else 0
    avg_profit = total_profit / num_episodes

    print(f"Average Reward over {num_episodes} episodes: {avg_reward}")
    print(f"Accuracy over {num_episodes} episodes: {accuracy}")
    print(f"Average Profit over {num_episodes} episodes: {avg_profit}")

def main():
    # Define the file path to the prepared data
    file_path = './data/processed/MarketData_Prepared.tsv'  # Updated path

    # Load the prepared data
    data = load_prepared_data(file_path)

    # Print column names for debugging
    print("Column names in the dataset:", data.columns)

    # Define the target column (e.g., 'Close' or any other column you want to predict)
    target_column = 'Close'  # Update this with the correct column name

    # Train Random Forest for feature selection
    features = data.drop(columns=[target_column])
    target = data[target_column]
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(features, target)
    feature_importance = pd.Series(rf.feature_importances_, index=features.columns).sort_values(ascending=False)
    top_features = feature_importance.head(9).index.tolist()  # Select top 9 features

    # Ensure 'Close' column is included in the selected features
    if 'Close' not in top_features:
        top_features.append('Close')

    # Use top features for your RL model
    selected_data = data[top_features]

    # Create the custom environment
    env = DummyVecEnv([lambda: Monitor(CustomEnv(selected_data))])

    # Check if a GPU is available and set the device accordingly
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Define the RL algorithm (e.g., PPO) and move it to the GPU
    model = PPO('MlpPolicy', env, verbose=1, device=device)

    # Define the evaluation environment
    eval_env = DummyVecEnv([lambda: Monitor(CustomEnv(selected_data))])

    # Define the callback
    eval_callback = EvalCallback(
        eval_env, 
        best_model_save_path='./logs/best_model',
        log_path='./logs/', 
        eval_freq=5000, 
        deterministic=True, 
        render=False
    )

    # Configure TensorBoard logger
    new_logger = configure('./logs/', ["stdout", "tensorboard"])
    model.set_logger(new_logger)

    # Train the RL agent with logging and callback
    model.learn(total_timesteps=20000, callback=eval_callback)

    # Load the best model
    best_model_path = "./logs/best_model/best_model.zip"
    best_model = PPO.load(best_model_path, device=device)

    # Evaluate the best model
    evaluate_model(best_model, env)

    # Test the best model
    obs = env.reset()
    for iteration in range(1000):
        action, _states = best_model.predict(obs)
        obs, rewards, dones, infos = env.step(action)
        info = infos[0] if isinstance(infos, list) else infos
        print(f"Iteration: {iteration}, Action: {action}, Reward: {rewards}, Balance: {env.get_attr('balance')[0]}")
        env.render()

if __name__ == "__main__":
    main()