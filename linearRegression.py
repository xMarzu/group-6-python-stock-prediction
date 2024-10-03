import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import yfinance as yf
from sklearn.metrics import r2_score

# Download stock price data
def download_data(stock_symbol, start_date, end_date):
	# Adjust the end date to include the specified end date
	adjusted_end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)
	stock_data = yf.download(stock_symbol, start=start_date, end=adjusted_end_date.strftime('%Y-%m-%d'))
	stock_data.dropna(inplace=True)  # Handle missing data
	print(f"Data successfully fetched from {stock_data.index.min()} to {stock_data.index.max()}")  # Debug print
	return stock_data['Adj Close'], stock_data.index  # Return both prices and dates

# Preprocess data and create input sequences
def preprocess_data(data, sequence_length):
	sequences = []
	for i in range(len(data) - sequence_length):
		sequence = data.iloc[i:i + sequence_length].values  # Use .iloc for position-based indexing
		target = data.iloc[i + sequence_length]  # Use .iloc to properly get the target
		sequences.append((sequence, target))
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

# Predict next-day stock price
def predict_next_day_price(model, last_sequence, last_date):
	"""
	Predict the stock price for the next day using the last available sequence.
	"""
	predicted_price = model.predict(last_sequence.reshape(1, -1))[0]
	
	# Predict for the day after the last known date
	next_day = last_date + pd.Timedelta(days=1)
	return predicted_price, next_day

# Predict stock price for a specific date
def predict_for_date(model, stock_data, target_date, sequence_length):
	"""
	Predict the stock price for a specific date using the sequence ending on the previous trading day.
	"""
	if target_date not in stock_data.index:
		print(f"Target date {target_date} is not valid. Please verify if it is a past trading day.")
		return None, None
	
	target_index = stock_data.index.get_loc(target_date)
	if target_index < sequence_length:
		print(f"Not enough data to create a sequence for {target_date}.")
		return None, None
	
	sequence = stock_data.iloc[target_index-sequence_length:target_index].values
	actual_price = stock_data.loc[target_date]
	predicted_price = model.predict(sequence.reshape(1, -1))[0]
	
	return actual_price, predicted_price


def main():
	# Main Execution - Download stock data
	print("\n***Welcome to the Stock Price Prediction System!***")
	print("We will now fetch the historical stock price data for the specified stock symbol")
	stock_symbol = input("\nPlease enter the stock ticker that you wish to predict: ")
	print("We will now fetch the historical stock price data. Please enter the date range for fetching the stock data.")
	start_date = input("\nPlease enter the start date to fetch from (YYYY-MM-DD): ")
	end_date = input("\nPlease enter the end date to fetch to (YYYY-MM-DD): ")
	
	# Download data
	stock_data, dates = download_data(stock_symbol, start_date, end_date)

	# Preprocess data - Creates sequences of 10 days of stock prices
	sequence_length = 10
	data_sequences = preprocess_data(stock_data, sequence_length)

	# Split data into training and testing sets
	train_data, test_data = split_data(data_sequences)

	# Prepare training data
	training_x = np.array([item[0] for item in train_data])
	training_y = np.array([item[1] for item in train_data])

	# Train linear regression model
	model = train_model(training_x, training_y)

	# Menu for user choice
	print("\nChoose an option:\n")
	print("1. Predict the next trading day's stock price (one day after the last available data)")
	print("2. Backtest a specific date")
	choice = input("\nEnter your choice (1 or 2): ")

	if choice == '1':
		# Predict the next day's stock price using the last available sequence
		last_sequence = stock_data.iloc[-sequence_length:].values  # Last 10 days before the last available date
		last_date = dates[-1]  # The last date in the dataset

		# Debug prints
		print(f"\nData Sequence used for prediction: {last_sequence}")
		print(f"Last date in the dataset: {last_date}")

		# Predict stock price for the next day
		predicted_price, next_day = predict_next_day_price(model, last_sequence, last_date)

		# Output the predicted price for the next day
		print(f"\nPredicted Stock Price for {next_day.date()}, or next possible trading day: ${predicted_price:.2f}")

		# Optionally, calculate R-squared score on the test set
		testing_x = np.array([item[0] for item in test_data])
		testing_y = np.array([item[1] for item in test_data])
		y_pred = model.predict(testing_x)
		r2 = r2_score(testing_y, y_pred)
		print("\n*** Model Performance on Test Data ***")
		print(f"R-squared score: {r2:.4f}")
		print("Explanation: The R-squared (R²) score measures how well the model predicts stock prices.")
		print("An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate.\n")

	elif choice == '2':
		# Backtesting feature
		backtest_date = input("\nEnter a date for backtesting (YYYY-MM-DD): ")
		backtest_date = pd.to_datetime(backtest_date)
		actual_price, predicted_price = predict_for_date(model, stock_data, backtest_date, sequence_length)
		
		if actual_price is not None and predicted_price is not None:
			print(f"Actual Stock Price for {backtest_date.date()}: ${actual_price:.2f}")
			print(f"Predicted Stock Price for {backtest_date.date()}: ${predicted_price:.2f}")
			
            # Optionally, calculate R-squared score on the test set
			testing_x = np.array([item[0] for item in test_data])
			testing_y = np.array([item[1] for item in test_data])
			y_pred = model.predict(testing_x)
			r2 = r2_score(testing_y, y_pred)
			print("\n*** Model Performance on Test Data ***")
			print(f"R-squared score: {r2:.4f}")
			print("Explanation: The R-squared (R²) score measures how well the model predicts stock prices.")
			print("An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate.\n")
	else:
		print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
	main()