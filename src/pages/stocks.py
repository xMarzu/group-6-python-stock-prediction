import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

##stocks page
dash.register_page(__name__, )

stocks=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Define the table header
header = [html.Thead(html.Tr([html.Th("Stock Name"),html.Th("Stock Link")]))]

# Define the table body
body = html.Tbody(
    [html.Tr([html.Td(stock),html.Td(dbc.Button(f"{stock}", color="primary", class_name="mx-1",href=f"/stocks/{stock}"))]) for stock in stocks]
)

#Create table for filtered stocks
def create_table_body(filtered_stocks):
    return html.Tbody(
        [html.Tr([html.Td(stock), 
                   html.Td(dbc.Button(stock, color="primary", class_name="mx-1", href=f"/stocks/{stock}"))]) 
                  for stock in filtered_stocks]
    )
tablebody=create_table_body(stocks)

#Forming the table
table = dbc.Table(header + [tablebody], bordered=True, striped=True, hover=True, id="stock-table")

layout = html.Div([
    html.H1('This is our Stocks page'),
    html.Div('This is our Stocks page content.'),
    dcc.Input(id='search-bar', type='text', placeholder='Search for a stock...', className='mb-3'),
    table

    

  
])
# Callback to filter stocks based on search input
@dash.callback(
    Output('stock-table', 'children'),
    Input('search-bar', 'value')
)

def update_table(search_value):
    # Filter stocks based on search input
    if search_value:
        filtered_stocks = [stock for stock in stocks if search_value.upper() in stock]
    else:
        filtered_stocks = stocks
    
    # Return updated table body
    return header + [create_table_body(filtered_stocks)]