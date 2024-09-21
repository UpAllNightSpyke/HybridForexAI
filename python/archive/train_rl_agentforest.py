import warnings
warnings.filterwarnings("ignore", message="You tried to call render() but no `render_mode` was passed to the env constructor.")

import torch
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from custom_env import CustomEnv, load_prepared_data
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def evaluate_model(model, env, num_episodes=10):
    all_rewards = []
    correct_actions = 0
    total_actions = 0

    for episode in range(num_episodes):
        obs = env.reset()
        episode_rewards = 0
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, infos = env.step(action)
            episode_rewards += rewards

            # Unpack the info dictionary from the list
            info = infos[0] if isinstance(infos, list) else infos

            # Debug print statements
            print(f"Episode: {episode}, Action: {action}, Correct Action: {info.get('correct_action')}")

            # Custom accuracy calculation (example)
            # Assuming that the correct action is stored in the 'info' dictionary
            if 'correct_action' in info:
                correct_actions += (action == info['correct_action'])
            total_actions += 1

        all_rewards.append(episode_rewards)

    avg_reward = sum(all_rewards) / num_episodes
    accuracy = correct_actions / total_actions if total_actions > 0 else 0

    print(f"Average Reward over {num_episodes} episodes: {avg_reward}")
    print(f"Accuracy over {num_episodes} episodes: {accuracy}")

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
    env = DummyVecEnv([lambda: CustomEnv(selected_data)])
    env = VecNormalize(env, norm_obs=True, norm_reward=True)

    # Check if a GPU is available and set the device accordingly
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Define the RL algorithm (e.g., PPO) and move it to the GPU
    model = PPO('MlpPolicy', env, verbose=1, device=device)

    # Train the RL agent
    model.learn(total_timesteps=10000)

    # Save the trained model
    model.save("ppo_custom_env")

    # Load the trained model
    model = PPO.load("ppo_custom_env", device=device)

    # Evaluate the trained model
    evaluate_model(model, env)

    # Test the trained model
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, infos = env.step(action)
        info = infos[0] if isinstance(infos, list) else infos
        print(f"Test Action: {action}, Test Correct Action: {info.get('correct_action')}")
        env.render()

if __name__ == "__main__":
    main()
