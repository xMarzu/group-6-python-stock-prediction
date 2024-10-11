
import dash
from dash import html, dcc
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from dash import dash_table
from constants import STOCK_LIST
from src.components.home.top_gainer_loser import get_top_loser_gainer
dash.register_page(__name__, path='/')


@callback([Output("top-gainer-table", "data"), Output("top-loser-table", "data")], Input("top-gainer-table", "id"))
def load_loser_gainer(id):
    top_gainer, top_loser = get_top_loser_gainer()  
    return top_gainer.to_dict("records"), top_loser.to_dict("records")


@callback(
    Output("search-div", "children"),
    Input("search-input", "value")
)
def update_stock_list(search_value):
    if search_value is None or search_value == "":
        # If no input is given, display all stocks or a subset of them
        filtered_stocks = STOCK_LIST[:5]  # Show first 10 stocks by default
    else:
        # Filter stocks based on the search value (case-insensitive)
        search_value = search_value.upper()
        filtered_stocks = [stock for stock in STOCK_LIST if search_value in stock]
        filtered_stocks = filtered_stocks[:5]  # Show first 10 stocks by default
    
    # Create a list of html.A elements with filtered stocks
    return [html.A(html.P(stock), href=f"/stocks/{stock}") for stock in filtered_stocks]

layout = html.Div([
    html.Div(
        [
            html.P("Welcome to Stonks Analysis", className="font-mono text-5xl font-bold"),
            html.P("Search for your favourite stocks below here"),
            
            html.Div(
                [
                    html.Div([
                        html.Img(src='/assets/search.png', style={'height': '16px'} ),
                        dcc.Input(id="search-input", type="text", placeholder="Stock symbol" , className="p-2" , ),
                        html.Hr()
                    ], className="flex px-2 py-1 bg-white text-xl items-center"),
                    html.Div([
                       
                    ], className="text-left text-[15px] bg-white px-2 flex flex-col gap-1 text-blue-300", id="search-div")
                    
                ],
            ),
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
                        data=[],  # Pass the data to the table
                        style_table={'width': '50%'},  # Customize width as needed
                        style_cell={
                            'textAlign': 'center',  # Align text
                            'font_family': 'Arial',
                            'font_size': '16px',
                        },
                        
                        ), 
                    ], className="flex flex-col gap-4"
                    
                   )
                    
                ], className="flex gap-4"
            )
               
        ], className="text-3xl  flex flex-col items-center justify-center text-center gap-4"
    )
    
], className="")