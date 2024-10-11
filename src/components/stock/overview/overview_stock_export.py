import os
import yfinance as yf

# Download CSV file containing stock data into users download folder
def downloadCSV(ticker,period):
    """Downloads the current ticker info into the user's downloads folder

    Args:
        ticker (string): Current Ticker
        period (string): Period of time
    """
    try:
        #Download stock data from yfinance for the specific stock ticker and period
        data = yf.download(tickers=ticker,period = period)

        #Set download path for user's download folder
        download_folder = os.path.expanduser('~/Downloads')
        csv_file_path = os.path.join(download_folder, f'{ticker}_data.csv')

        #Save the downloaded data into a CSV file
        data.to_csv(csv_file_path)

        print(f"Data for {ticker} saved to {csv_file_path}")

    except:
        print(f'Error downloading data for {ticker}')

