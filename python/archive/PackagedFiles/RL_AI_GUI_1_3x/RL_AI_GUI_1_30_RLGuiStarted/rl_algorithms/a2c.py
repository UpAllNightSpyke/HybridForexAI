from stable_baselines3 import A2C

def train_a2c(env, **kwargs):
    model = A2C('MlpPolicy', env, **kwargs)
    model.learn(total_timesteps=kwargs.get('total_timesteps', 10000))
    return model

algorithm_params = {
    'learning_rate': 0.0007,
    'n_steps': 5,
    'gamma': 0.99,
    'gae_lambda': 1.0,
    'ent_coef': 0.01,
    'vf_coef': 0.5,
    'max_grad_norm': 0.5,
    'total_timesteps': 10000
}