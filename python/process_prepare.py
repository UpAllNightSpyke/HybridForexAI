import os
from preprocess import load_raw_data, preprocess_data, save_preprocessed_data
from data_preparation import load_preprocessed_data, prepare_data_for_training, save_prepared_data

def main(input_file):
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = input_file
    preprocessed_data_path = os.path.join(script_dir, '..', 'data', 'intermediate', 'MarketData_Preprocessed.csv')
    prepared_data_path = os.path.join(script_dir, '..', 'data', 'processed', 'MarketData_Prepared.tsv')

    # Step 1: Preprocess the raw data
    raw_data = load_raw_data(raw_data_path)
    
    # Debugging: Print columns of raw data
    print("Columns in raw data:", raw_data.columns)
    
    preprocessed_data = preprocess_data(raw_data)
    save_preprocessed_data(preprocessed_data, preprocessed_data_path)

    # Step 2: Prepare the data for training
    preprocessed_data = load_preprocessed_data(preprocessed_data_path)
    prepared_data = prepare_data_for_training(preprocessed_data)
    save_prepared_data(prepared_data, prepared_data_path)

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'MarketData.csv')
    main(input_file)