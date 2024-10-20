from stable_baselines3 import DQN

def train_dqn(env, **kwargs):
    model = DQN('MlpPolicy', env, **kwargs)
    model.learn(total_timesteps=kwargs.get('total_timesteps', 10000))
    return model

algorithm_params = {
    'learning_rate': 0.001,
    'buffer_size': 100000,
    'learning_starts': 1000,
    'batch_size': 32,
    'tau': 0.005,
    'gamma': 0.99,
    'train_freq': 4,
    'gradient_steps': 1,
    'total_timesteps': 10000
}