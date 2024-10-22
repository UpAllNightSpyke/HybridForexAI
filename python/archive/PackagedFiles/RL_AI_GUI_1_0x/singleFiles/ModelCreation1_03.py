import os  # Import the os module for interacting with the operating system
import pandas as pd  # Import pandas for data manipulation and analysis

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
    data['AlligatorJaw'] = data['AlligatorJaw'].fillna(data['AlligatorJaw'].mean()).infer_objects(copy=False)
    data['AlligatorTeeth'] = data['AlligatorTeeth'].fillna(data['AlligatorTeeth'].mean()).infer_objects(copy=False)
    data['AlligatorLips'] = data['AlligatorLips'].fillna(data['AlligatorLips'].mean()).infer_objects(copy=False)
    data['RSI'] = data['RSI'].fillna(data['RSI'].mean()).infer_objects(copy=False)
    
    return data  # Return the prepared data

# Example usage
if __name__ == "__main__":
    # This block will only run if the script is executed directly, not if it is imported as a module
    
    # Define the path to the TSV file in the MT5 common folder
    file_path = r'C:\Users\spyke\AppData\Roaming\MetaQuotes\Terminal\Common\Files\data\raw\MarketData_LastWeek.tsv'
    
    # Load the TSV file using the load_tsv function
    data = load_tsv(file_path)
    
    # Prepare the data using the prepare_data function
    prepared_data = prepare_data(data)
    
    # Define the path to save the prepared data in the data/processed folder within the HybridForexAI project directory
    prepared_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'PreparedModelData.tsv')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(prepared_data_path), exist_ok=True)
    
    # Save the prepared data to a CSV file
    prepared_data.to_csv(prepared_data_path, index=False, sep='\t')
    print(f"Prepared data saved to {prepared_data_path}")