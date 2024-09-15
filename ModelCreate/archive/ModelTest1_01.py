import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os

def load_prepared_data(file_path):
    data = pd.read_csv(file_path, delimiter='\t')
    print("Successfully loaded prepared data.")
    return data

def train_and_evaluate_model(data):
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MovingAverage', 'AlligatorJaw', 'AlligatorTeeth', 'AlligatorLips', 'RSI']
    target = 'Close'  # Example target variable

    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    print(predictions.head())

def main():
    file_path = os.path.join(os.getcwd(), 'ModelCreate', 'PreparedData', 'PreparedModelData.tsv')
    data = load_prepared_data(file_path)
    train_and_evaluate_model(data)

if __name__ == "__main__":
    main()