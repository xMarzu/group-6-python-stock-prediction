import dash
from dash import html, dcc
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from constants import STOCK_LIST
dash.register_page(__name__, path='/')


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
                
            )
               
        ], className="text-3xl h-[50vh] flex flex-col items-center justify-center text-center gap-4"
    )
    
], className="")