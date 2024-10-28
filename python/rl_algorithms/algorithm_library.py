from enum import Enum

algorithm_params = {  # Define algorithm_params here
    "dmc": {
        "params": {
            "order": 3,
            "iterations": 100,
            "horizon": 10,
            "total_timesteps": 10000
        },
        "module_path": "rl_algorithms.model_based.dmc"
    },
    "dtmc": {
        "params": {
            "order": 3,
            "iterations": 100,
            "horizon": 10,
            "total_timesteps": 10000
        },
        "module_path": "rl_algorithms.model_based.dtmc"
    },
    "dqn": {
        "params": {
            "learning_rate": 0.001,
            "buffer_size": 100000,
            "learning_starts": 1000,
            "batch_size": 32,
            "tau": 0.005,
            "gamma": 0.99,
            "train_freq": 4,
            "gradient_steps": 1,
            "total_timesteps": 10000
        },
        "module_path": "rl_algorithms.value_based.dqn"
    },
    "a2c": {
        "params": {
            "learning_rate": 0.0007,
            "n_steps": 5,
            "gamma": 0.99,
            "gae_lambda": 1.0,
            "ent_coef": 0.01,
            "vf_coef": 0.5,
            "max_grad_norm": 0.5,
            "total_timesteps": 10000
        },
        "module_path": "rl_algorithms.policy_based.a2c"
    },
    "ppo": {
        "params": {
            "learning_rate": 0.0003,
            "n_steps": 2048,
            "batch_size": 64,
            "n_epochs": 10,
            "gamma": 0.99,
            "gae_lambda": 0.95,
            "clip_range": 0.2,
            "total_timesteps": 10000
        },
        "module_path": "rl_algorithms.policy_based.ppo"
    }
}

class AlgorithmType(Enum):
    DQN = 'DQN'
    PPO = 'PPO'
    A2C = 'A2C'
    # Add more algorithms as needed