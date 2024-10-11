import requests
from bs4 import BeautifulSoup
import pandas as pd
from dash import html, callback, Output,  Input, dcc,ctx, ALL, dash_table






def scrape_yahoo_finance(url):
    """Scapes yahoo finance page

    Args:
        url (str): URL you want to scrape from 

    Returns:
        DataFrame: Dataframe of scraped data
    """
    
    
    # Send a request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data from {url}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table with the stock data
    table = soup.find('table', {'class': 'markets-table'})
    if table is None:
        print(f"No data found at {url}")
        return None
    
    # Extract table headers (the stock data headers)
    headers = [header.text.strip() for header in table.find('thead').find_all('th')]
    
    # Extract the table rows (each row represents a stock)
    rows = []
    for row in table.find('tbody').find_all('tr'):
        cells = [cell.text for cell in row.find_all('td')]
        rows.append(cells)
    
    # Create a DataFrame from the extracted rows
    df = pd.DataFrame(rows, columns=headers)
    
    return df

def get_top_loser_gainer():
    """Gets the top losers and gainers in the stock market based on Yahoo Finance
    """
    
    # Function to clean and format the price column
    def format_price(price_str):
    # Split the price string by space and take the first part (price)
        price = price_str.split()[0]
        # Add the dollar sign before the price
        return f"${price}"



    # URLs for gainers and losers on Yahoo Finance
    gainers_url = 'https://finance.yahoo.com/markets/stocks/gainers/'
    losers_url = 'https://finance.yahoo.com/markets/stocks/losers/'

    # Scrape the top gainers
    top_gainers = scrape_yahoo_finance(gainers_url)
   
    
    top_gainers = top_gainers.head(5)
    
    top_gainers = top_gainers[["Symbol", "Price", "Change %", "Market Cap"]]
    top_gainers["Price"] = top_gainers["Price"].apply(format_price)
   


    # Scrape the top losers
    top_losers = scrape_yahoo_finance(losers_url)
    top_losers = top_losers.head(5)
    top_losers = top_losers[["Symbol", "Price", "Change %", "Market Cap"]]
    top_losers["Price"] = top_losers["Price"].apply(format_price)
    return top_gainers, top_losers



##Callback for returning the top gainers and top losers into the data proeprty of dash tables
@callback([Output("top-gainer-table", "data"), Output("top-loser-table", "data")], Input("top-gainer-table", "id"))
def load_loser_gainer(id):
    top_gainer, top_loser = get_top_loser_gainer()  
    return top_gainer.to_dict("records"), top_loser.to_dict("records")



def generate_top_loser_gainer():
    """Generates a top loser/gainer layout
    """
    return (
        html.Div(
                [
                   html.Div(
                    [
                        html.H3("Top Gainers"),
                        dash_table.DataTable(
                        id='top-gainer-table',
                        columns=[
                            {'name': 'Symbol', 'id': 'Symbol'},
                            {'name': 'Price', 'id': 'Price'},
                            {'name': 'Change %', 'id': 'Change %'},
                            {'name': 'Market Cap', 'id': 'Market Cap'}
                        ],
                        data=[],  # Pass the data to the table
                        style_table={'width': '50%'},  # Customize width as needed
                        style_cell={
                            'textAlign': 'center',  # Align text
                            'font_family': 'Arial',
                            'font_size': '16px',
                            "padding" : "8px"
                        },
                        
                        ), 
                    ], className="flex flex-col gap-4"
                    
                   ),
                   html.Div(
                    [
                        html.H3("Top Losers"),
                        dash_table.DataTable(
                        id='top-loser-table',
                        columns=[
                             {'name': 'Symbol', 'id': 'Symbol'},
                            {'name': 'Price', 'id': 'Price'},
                            {'name': 'Change %', 'id': 'Change %'},
                            {'name': 'Market Cap', 'id': 'Market Cap'}
                        ],
                        data=[],  #Data that will be input from the callback 
                        style_table={'width': '50%'},  
                        style_cell={
                            'textAlign': 'center',  
                            'font_family': 'Arial',
                            'font_size': '16px',
                             "padding" : "8px"
                        },
                        
                        ), 
                    ], className="flex flex-col gap-4"
                    
                   )
                    
                ], className="flex gap-4"
            )
    )