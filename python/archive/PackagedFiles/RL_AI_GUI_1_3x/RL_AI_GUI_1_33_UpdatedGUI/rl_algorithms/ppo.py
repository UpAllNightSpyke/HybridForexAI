from stable_baselines3 import PPO

def train_ppo(env, **kwargs):
    model = PPO('MlpPolicy', env, **kwargs)
    model.learn(total_timesteps=kwargs.get('total_timesteps', 10000))
    return model

algorithm_params = {
    'learning_rate': 0.0003,
    'n_steps': 2048,
    'batch_size': 64,
    'n_epochs': 10,
    'gamma': 0.99,
    'gae_lambda': 0.95,
    'clip_range': 0.2,
    'total_timesteps': 10000
}