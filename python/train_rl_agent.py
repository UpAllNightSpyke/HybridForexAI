import torch
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from custom_env import CustomEnv, load_prepared_data

def main():
    # Define the file path to the prepared data
    file_path = '../data/processed/MarketData_Prepared.tsv'

    # Load the prepared data
    data = load_prepared_data(file_path)

    # Create the custom environment
    env = DummyVecEnv([lambda: CustomEnv(data)])
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

    # Test the trained model
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()

if __name__ == "__main__":
    main()