import os
import pickle
from appdirs import user_data_dir
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from rl_algorithms.functions import initialize_algorithms, get_available_algorithms
from ai_utils.train_hmm import load_hmm_model
from ai_utils.ai_env import TradingEnv  # Import the TradingEnv class
from lxml import etree

def find_raw_data():
    """
    Locates the raw data file in the user data directory and extracts symbol and timeframe from the filename.

    Returns:
        str: The path to the raw data file, symbol, and timeframe.

    Raises:
        FileNotFoundError: If no raw data file is found.
    """
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
    raw_data_dir = os.path.join(user_data_path, 'forex_data', 'raw')

    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".csv"):
            raw_data_file = os.path.join(raw_data_dir, filename)
            
            # Extract symbol and timeframe from filename
            try:
                symbol, timeframe, _, _ = filename[:-4].split('_')  # Remove '.csv' and split
                return raw_data_file, symbol, timeframe
            except ValueError:
                print(f"Skipping file with invalid name: {filename}")

    raise FileNotFoundError("No raw data file found.")

def train_rl_model(algorithm_type, use_hmm=False):
    try:
        # Print the algorithm type
        print(f"Training RL model with algorithm type: {algorithm_type}")

        # 1. Load the raw data
        raw_data_file, symbol, timeframe = find_raw_data()  # Get symbol and timeframe
        data = pd.read_csv(raw_data_file)

        # 2. Remove rows with NaN values
        data.dropna(inplace=True)

        # 3. Feature engineering for time-based features (using datetime)
        data['time'] = pd.to_datetime(data['time'])
        data['hour_of_day'] = data['time'].dt.hour
        data['day_of_week'] = data['time'].dt.dayofweek

        # 4. Normalize the data (including indicator columns)
        indicator_columns = [col for col in data.columns if col not in ['time', 'hour_of_day', 'day_of_week']]
        scaler = MinMaxScaler()
        data[indicator_columns] = scaler.fit_transform(data[indicator_columns])

        # 5. Conditionally incorporate HMM states if use_hmm is True
        if use_hmm:
            hmm_model = load_hmm_model()
            if hmm_model is None:
                raise ValueError("HMM model not found. Please train or load an HMM model first.")

            # Use only the necessary columns for HMM prediction
            hmm_data = data[['open', 'high', 'low', 'close', 'tick_volume', 'hour_of_day', 'day_of_week']].values
            hidden_states = hmm_model.predict(hmm_data)
            data['hidden_state'] = hidden_states

            # Select all relevant columns for RL training (including hidden states, time features, and indicator data)
            rl_data = data.drop(columns=['time']).values
        else:
            # Select relevant columns for RL training (including time features and indicator data)
            rl_data = data[['open', 'high', 'low', 'close', 'tick_volume', 'hour_of_day', 'day_of_week'] + indicator_columns].values

        # 6. Initialize the RL environment
        env = TradingEnv(rl_data, symbol, timeframe)  # Pass symbol and timeframe to TradingEnv

        # 7. Initialize and train the RL model
        algorithm_params = initialize_algorithms()  # Get algorithm_params
        available_algorithms = get_available_algorithms()  # Get the available algorithms

        # Check if the algorithm_type is valid
        if algorithm_type not in available_algorithms:
            raise ValueError(f"Invalid algorithm type: {algorithm_type}")

        # Access the algorithm function using the algorithm_type as the key
        algorithm = available_algorithms[algorithm_type]  

        # Instantiate the model using the algorithm function
        model = algorithm(env, **algorithm_params[algorithm_type.lower()]['params'])  # Pass the parameters here

        model.learn(total_timesteps=10000)  # Adjust total_timesteps as needed

        # 8. Save the trained RL model
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'RLmodel')
        os.makedirs(model_dir, exist_ok=True)
        model_filename = os.path.join(model_dir, f'rl_model_{algorithm_type}.zip')

        # Use the model's save method
        model.save(model_filename)

        print(f"RL model ({algorithm_type}) trained and saved successfully!")

    except Exception as e:
        print(f"An error occurred while training the RL model: {e}")

def load_rl_model(algorithm_type):
    try:
        # Print the algorithm type
        print(f"Loading RL model with algorithm type: {algorithm_type}")

        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'RLmodel')
        model_filename = os.path.join(model_dir, f'rl_model_{algorithm_type}.zip')

        # Get available algorithms dynamically
        available_algorithms = get_available_algorithms()  # Get the available algorithms

        # Check if the algorithm type is valid
        if algorithm_type not in available_algorithms:
            raise ValueError(f"Invalid algorithm type: {algorithm_type}")

        # Load the model using the corresponding algorithm class
        model = available_algorithms[algorithm_type].load(model_filename)

        print(f"RL model ({algorithm_type}) loaded successfully!")
        return model

    except FileNotFoundError:
        print(f"Trained RL model ({algorithm_type}) not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the RL model: {e}")
        return None