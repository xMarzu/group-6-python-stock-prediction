from dash import html, callback, Output,  Input, dcc,ctx, ALL

def stock_tabs(stock_id : str):
    """Generates the stock tabs for header layout

    Args:
        stock_id (str): Current stock ID
    
    """
    return (
        html.Div(
            [
                html.A(
                    html.Button("Overview"),
                    href=f"/stocks/{stock_id}"
                ),
                html.A(
                    html.Button("Backtesting"),
                    href=f"/stocks/{stock_id}/backtesting"
                ),
                html.A(
                    html.Button("Prediction"),
                    href=f"/stocks/{stock_id}/prediction"
                ),
                
                
                
            ], className="flex gap-4 text-blue-400"
        )
    )