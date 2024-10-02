from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.stock_layout_functions import get_stock_id_from_url
from src.components.stock.overview.overview_indicators import generate_overview_indicators
from src.components.stock.overview.overview_chart_component import generate_chart_component
    


def overview_layout(stock_id : str):
    """Returns the whole overview tab

    Args:
        stock_id (str): Current stock ID
    """
    
    return (
        html.Div
        (
            [
                dcc.Store(id='overview-store'),
                dcc.Store(id="chart-store"),
                html.Div(
                    [
                        generate_overview_indicators(stock_id=stock_id),
                        generate_chart_component()
                         
                    ],className="flex gap-8"
                )
                
            ]
           
        )
       
    
    )
    
    