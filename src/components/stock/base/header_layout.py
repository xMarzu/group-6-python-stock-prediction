from dash import html, callback, Output,  Input, dcc,ctx, ALL
"""
This file contains the header layout for the base layout of all single stocks
"""


"""
Callback for changing colour of difference text when its positive/negative
"""
@callback(Output("stock-difference-header", "style"), Input("header-store", "data"))
def difference_color(data :dict):
    """ Returns style based on whether the value is pos/negative
    Args:
        data (dict): Dictionary containing difference key

    Returns:
        style (dict[str,str]): Style of color
    """
    
    if (data["difference"] >= 0):
        return {"color" : "green"}
    else:
        return {"color" : "red"}
    
"""
Callback for title, close and difference of stocks
"""    
@callback ([Output("stock-title", "children"),Output("stock-close-header", "children"), Output("stock-difference-header", "children")], Input("header-store", "data"))
def assign_headers(data):
    """ Returns header values from dictionary
    Args:
        data (dict): Dictionary containing header values

    Returns:
        stock_title, close_price, difference
    """
    print("Fetching header data: ", data)
    stock_name = data["stock_name"]
    stock_id = data["stock_id"]
    close_price = f'{data["close"]:.3f}'
    stock_difference =  data["difference"]
    if (stock_difference > 0):
        stock_difference = f"+{stock_difference:.2f}"
    else:
        stock_difference = f"{stock_difference:.2f}"
    stock_difference_percentage = data["percentage_difference"]
    stock_title = f"{stock_name} ({stock_id})"
    difference = f"{stock_difference} ({stock_difference_percentage:.2f}%)"
    return stock_title, close_price, difference

def header_layout():
    """ 
    Returns header layout for single stock base       
    """

    return (
      
        html.Div
        (
            
            [
                dcc.Store(id='header-store'),
                html.H1([], className="text-xl text-mono font-bold", id="stock-title"),
                html.Div
                (
                    [
                    html.Div
                    (
                        [
                        html.H2([], className="text-4xl text-mono font-bold" , id="stock-close-header"),
                        html.P([], className="text-lg   text-mono", id="stock-difference-header")
                        ],className="flex gap-2"
                    ),
                    html.P("At Close: Sep 27, 2024, 4:00PM" , className="text-md")
                    
                    ], 
                ),
                
                
                
            ], className="flex flex-col gap-4"
        )
    )