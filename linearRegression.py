# Before running, install dependencies: pip install numpy scikit-learn yfinance

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import yfinance as yf
from sklearn.metrics import r2_score

# Download stock price data
def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    print(stock_data)
    return stock_data['Adj Close'], stock_data.index  # Return both prices and dates

# Preprocess data and create input sequences
def preprocess_data(data, dates, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        sequence = data[i:i+sequence_length].values
        target = data[i+sequence_length]
        date = dates[i+sequence_length]
        sequences.append((sequence, target, date))
    return sequences

# Split data into training and testing sets
def split_data(data, test_size=0.2):
    train_data, test_data = train_test_split(data, test_size=test_size, shuffle=False)
    return train_data, test_data

# Train linear regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Main Execution - Download stock data
ticker = 'NVDA'
start_date = '2014-01-01'
end_date = '2024-09-17'
stock_data, dates = download_stock_data(ticker, start_date, end_date)

# Preprocess data - Creates sequences of 10 days of stock prices, target on the 11th day
sequence_length = 10
data_sequences = preprocess_data(stock_data, dates, sequence_length)

# Split data into training and testing sets
train_data, test_data = split_data(data_sequences)

# Prepare training data
X_train = np.array([item[0] for item in train_data])
y_train = np.array([item[1] for item in train_data])

# Prepare testing data
X_test = np.array([item[0] for item in test_data])
y_test = np.array([item[1] for item in test_data])
test_dates = [item[2] for item in test_data]  # Extract dates for test data

# Train linear regression model
model = train_model(X_train, y_train)

# Example of using the trained model for prediction
specific_date = '2024-08-26'  # Example date; change as needed
specific_index = dates.get_loc(specific_date)

# Ensure the index is valid
if specific_index < sequence_length or specific_index >= len(stock_data):
    raise ValueError("Date is too close to the beginning or end of the data for prediction.")

# Prepare the sequence for the specific date
sequence = stock_data.iloc[specific_index-sequence_length:specific_index].values
sequence = sequence.reshape(1, -1)

# Predict
predicted_price = model.predict(sequence)[0]
prediction_date = dates[specific_index]  # Date of prediction

# Output the stock price for the specific date and prediction
print(f"Stock Price on {specific_date}: ${stock_data[specific_date]:.2f}")
print(f"Predicted Stock Price for {prediction_date.date()}: ${predicted_price:.2f}")

# Predict the values for the test set
y_pred = model.predict(X_test)

# Calculate the R-squared score
r2 = r2_score(y_test, y_pred)

# Print the R-squared score
print(f"R-squared score: {r2:.4f}")

