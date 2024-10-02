# remember to pip install python-dotenv
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to fetch stock news from Alpha Vantage API
def fetch_stock_news(ticker):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  # Fetch API key from environment variable
    
    if not api_key:
        raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable with your API key.")
    
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",  # Alpha Vantage news sentiment function
        "tickers": ticker,             # Stock ticker for the news
        "apikey": api_key              # Your API key from environment
    }

    # Make the API request
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        # Return the JSON response if successful
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to format the stock news data
def format_stock_news(news_data):
    if not news_data:
        print("There are no news data available.")
        return
    
    print(f"Total Articles: {news_data.get('items')}")
    print(f"Sentiment Score Definitions: {news_data.get('sentiment_score_definition')}")
    print(f"Relevance Score Definitions: {news_data.get('relevance_score_definition')}")
    print("\n--- Latest Stock News ---\n")
    
    for article in news_data.get('feed', []):
        title = article['title']
        url = article['url']
        time_published = article['time_published']
        authors = ", ".join(article.get('authors', []))
        source = article['source']
        summary = article.get('summary', 'No summary available.')
        sentiment_label = article['overall_sentiment_label']
        sentiment_score = article['overall_sentiment_score']
        
        # Print the news article
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Published on: {time_published}")
        print(f"Authors: {authors}")
        print(f"Source: {source}")
        print(f"Summary: {summary}")
        print(f"Sentiment Label: {sentiment_label}")
        print(f"Sentiment Score: {sentiment_score}")
        print("\n")

# Main function to run the program
def main():
    ticker = input("Enter the stock symbol (e.g., AAPL, TSLA): ")
    
    # Fetch the news data
    stock_news_data = fetch_stock_news(ticker)
    
    # Format and display the news data
    format_stock_news(stock_news_data)

if __name__ == "__main__":
    main()
