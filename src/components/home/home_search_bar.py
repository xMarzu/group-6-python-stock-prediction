from dash import html, callback, Output,  Input, dcc,ctx, ALL
from constants import STOCK_LIST



#This file creates the search bar and contains the logic for the search bar
@callback(
    Output("search-div", "children"),
    Input("search-input", "value")
)
def update_stock_list(search_value):
    if search_value is None or search_value == "":
        #Default input, either none or empty
        filtered_stocks = STOCK_LIST[:5]  # Show first 5 stocks by default
    else:
        # Filter stocks based on the search value (case-insensitive)
        search_value = search_value.upper()
        filtered_stocks = [stock for stock in STOCK_LIST if search_value in stock]
        filtered_stocks = filtered_stocks[:5]  # Show the first 5 stocks that are matching
    # Create a list html anchors to return to the user with the stock name 
    return [html.A(html.P(stock), href=f"/stocks/{stock}") for stock in filtered_stocks]



   
def home_search_bar():
    """Creates a search bar 
    """
    return (
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
    )
    