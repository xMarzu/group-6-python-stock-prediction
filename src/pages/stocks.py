import dash
from dash import Dash,html,callback
from dash import html,dcc
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import yfinance as yf 
from concurrent.futures import ThreadPoolExecutor, as_completed 
from constants import STOCK_LIST
##stocks page
dash.register_page(__name__)


stocks=sorted(STOCK_LIST) 
tickers = yf.Tickers(' '.join(stocks)) 
stockDictionary = {} 
def fetch_stock_information(stock): 
    lst={} 
    ticker_info = tickers.tickers[stock].info 
    lst["Company_Name"]=ticker_info.get('longName', 'N/A') 
    lst["Industry"]=ticker_info.get('industry', 'N/A') 
    lst["Market_Cap"]=ticker_info.get('marketCap', 'N/A')  
    stockDictionary[stock]=lst 
    return stock,lst 
 
with ThreadPoolExecutor(max_workers=20) as executor: 
    # Submit tasks to the executor 
    futures = [executor.submit(fetch_stock_information, stock) for stock in stocks] 
     
    # As the tasks complete, store the results in the dictionary 
    for future in as_completed(futures): 
        stock, result = future.result() 
        stockDictionary[stock] = result 

# Columns for the AgGrid
columns = [
    {
        'headerName': "Stock Link",
        'field': "link",
        'cellRenderer': "StockLink",
        'cellRendererParams': {"className": "btn btn-info", "text": "View"}
    },
    {'headerName': "Company Name", 'field': "c_name"},
    {'headerName': "Industry", 'field': "industry"},
    {'headerName': "Market Cap", 'field': "m_cap"},
    
]

# Initial data preparation for AgGrid
def prepare_data():
    return [
        {"link": stock,"c_name":stockDictionary[stock]["Company_Name"],"industry":stockDictionary[stock]["Industry"],"m_cap":f"${stockDictionary[stock]['Market_Cap']}"}
        for stock in stockDictionary
    ]

#Layout for the page
layout = html.Div([
    dag.AgGrid(
        id='enable-pagination',
        columnDefs=columns,
        rowData=prepare_data(),
        defaultColDef={'sortable': True, 'filter': True, 'resizable': True},
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,  # Set the page size for pagination
            
        },
        

    )
])

