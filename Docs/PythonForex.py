import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load historical chart data
currency_data = pd.read_csv('currency_data.csv')
gold_data = pd.read_csv('gold_data.csv')
oil_data = pd.read_csv('oil_data.csv')
news_data = pd.read_csv('news_data.csv')

# Preprocess data
def preprocess_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

currency_data = preprocess_data(currency_data)
gold_data = preprocess_data(gold_data)
oil_data = preprocess_data(oil_data)
news_data = preprocess_data(news_data)

# Feature engineering
def create_features(df):
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    df['RSI'] = compute_rsi(df['Close'])
    return df

currency_data = create_features(currency_data)
gold_data = create_features(gold_data)
oil_data = create_features(oil_data)

# Combine features
combined_data = pd.concat([currency_data, gold_data, oil_data], axis=1)

# Encode news data
news_data['Sentiment'] = news_data['Sentiment'].apply(encode_sentiment)

# Merge news data with combined data
final_data = pd.merge(combined_data, news_data, left_index=True, right_index=True, how='left')

# Normalize data
scaler = StandardScaler()
final_data_scaled = scaler.fit_transform(final_data.dropna())

# Save preprocessed data
np.save('preprocessed_data.npy', final_data_scaled)