import os  # Import the os module for interacting with the operating system
import pandas as pd  # Import pandas for data manipulation and analysis
from sklearn.preprocessing import MinMaxScaler  # Import MinMaxScaler for normalizing data
from sklearn.metrics import mean_squared_error  # Import mean_squared_error for evaluating model performance
from sklearn.model_selection import train_test_split  # Import train_test_split for splitting data into training and testing sets
from sklearn.linear_model import LinearRegression  # Import LinearRegression model

def load_tsv(file_path):
    """
    Load a TSV (Tab-Separated Values) file into a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the TSV file.
    
    Returns:
    pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    # Check if the file exists at the given path
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")  # Print an error message if the file is not found
        return pd.DataFrame()  # Return an empty DataFrame if the file does not exist
    
    # Open the file in binary read mode
    with open(file_path, 'rb') as file:
        raw_data = file.read()  # Read the entire file content into raw_data
        # Determine the file encoding based on the byte order mark (BOM)
        if raw_data.startswith(b'\xef\xbb\xbf'):
            encoding = 'utf-8-sig'  # UTF-8 with BOM
        elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
            encoding = 'utf-16'  # UTF-16
        else:
            encoding = 'latin1'  # Default to Latin-1 encoding
    
    # Load the TSV file into a DataFrame using the determined encoding
    data = pd.read_csv(file_path, encoding=encoding, delimiter='\t')
    print(f"Successfully loaded TSV with encoding: {encoding}")  # Print a success message with the encoding used
    return data  # Return the loaded DataFrame

def prepare_data(data):
    """
    Prepare the data for model training by handling missing values and normalizing features.
    
    Parameters:
    data (pd.DataFrame): The raw data as a pandas DataFrame.
    
    Returns:
    pd.DataFrame: The prepared data as a pandas DataFrame.
    """
    # Define the features to be used in the model
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']
    
    # Replace zeros with NaN for specific columns to handle missing values
    data['AlligatorJaw'] = data['AlligatorJaw'].replace({0: pd.NA})
    data['AlligatorTeeth'] = data['AlligatorTeeth'].replace({0: pd.NA})
    data['AlligatorLips'] = data['AlligatorLips'].replace({0: pd.NA})
    data['RSI'] = data['RSI'].replace({0: pd.NA})
    
    # Fill NaN values with the mean of the respective columns
    data['AlligatorJaw'] = data['AlligatorJaw'].fillna(data['AlligatorJaw'].mean())
    data['AlligatorTeeth'] = data['AlligatorTeeth'].fillna(data['AlligatorTeeth'].mean())
    data['AlligatorLips'] = data['AlligatorLips'].fillna(data['AlligatorLips'].mean())
    data['RSI'] = data['RSI'].fillna(data['RSI'].mean())
    
    # Initialize the MinMaxScaler to normalize the feature columns
    scaler = MinMaxScaler()
    # Apply the scaler to the feature columns to scale them between 0 and 1
    data[features] = scaler.fit_transform(data[features])
    
    # Print the minimum values of the normalized features for verification
    print("Min values after normalization:")
    print(data[features].min())
    # Print the maximum values of the normalized features for verification
    print("Max values after normalization:")
    print(data[features].max())
    
    return data  # Return the prepared DataFrame

def train_model(data):
    """
    Train a linear regression model using the prepared data.
    
    Parameters:
    data (pd.DataFrame): The prepared data as a pandas DataFrame.
    
    Returns:
    LinearRegression: The trained linear regression model.
    """
    # Define the target variable and features
    target = 'Close'
    features = ['Open', 'High', 'Low', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)
    
    # Initialize the linear regression model
    model = LinearRegression()
    # Train the model using the training data
    model.fit(X_train, y_train)
    
    # Predict the target variable for the testing data
    y_pred = model.predict(X_test)
    # Calculate the mean squared error of the predictions
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")  # Print the mean squared error
    
    return model  # Return the trained model

def main():
    """
    Main function to load, prepare, train, and save the model.
    """
    # Define the path to the raw data file
    file_path = os.path.join(os.getcwd(), 'data', 'processed', 'PreparedModelData.tsv')
    print(f"Loading data from: {file_path}")  # Print the path of the file being loaded
    
    # Load the raw data
    data = load_tsv(file_path)
    
    # Debugging: Print the first few rows of the loaded data
    print("First few rows of the loaded data:")
    print(data.head())  # Print the first few rows to verify the data has been loaded correctly
    
    # Check if the DataFrame is empty
    if data.empty:
        print("The DataFrame is empty. Please check the file content and path.")  # Print an error message if the DataFrame is empty
        return  # Exit the function if the DataFrame is empty
    
    # Prepare the data
    data = prepare_data(data)
    
    # Train the model
    model = train_model(data)
    
    # Define the path to save the trained model
    model_file_path = os.path.join(os.getcwd(), 'models', 'python', 'TrainedModel.pkl')
    
    # Save the trained model to a file
    pd.to_pickle(model, model_file_path)  # Use pandas to save the model as a pickle file
    print(f"Model training complete. Trained model saved to '{model_file_path}'.")  # Print a success message with the path of the saved model

if __name__ == "__main__":
    main()  # Call the main function if this script is executed directly