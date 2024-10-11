from dash import html, callback, Output,  Input, dcc,ctx, ALL, State
from src.components.stock.stock_layout_functions import get_stock_id_from_url, get_stock_data
from src.components.stock.overview.overview_line_chart import generate_line_chart
from src.components.stock.overview.overview_candlestick import generate_candlestick_chart
import yfinance as yf
import plotly.graph_objs as go






##Callback for returning the candlestick/line graph based on the current chart store
@callback(Output("graph-container", "children"), [Input("chart-store", "data"), Input("swap-button", "n_clicks")])
def plot_chart(data, clicks):
    
    if data is None:
        pass
    else:
        if (clicks % 2 == 0):
            #If number of clicks is even, bring the line chart
            line_chart = generate_line_chart(data)
            return dcc.Graph(figure = line_chart)
        else:
            
            candlestick = generate_candlestick_chart(data)
            return dcc.Graph(figure=candlestick)


##Get the stock data when the user clicks on any of the graph buttons, 5d,1m,etc
@callback(Output("chart-store", "data"), [Input("url","pathname"), Input({'type':'graph-button', 'index':ALL, 'value': ALL},"n_clicks")] )
def store_chart_data(url: str, buttons):
    stock_id = get_stock_id_from_url(url=url)
    triggered = ctx.triggered_id
    ##get chart data and store
    if (triggered == "url"):
        data = get_stock_data(stock_id, "max")
    else:
        data = get_stock_data(stock_id, triggered["value"])
  
    return data

    

def generate_chart_component():
    
    base_chart = go.Figure()
    base_chart.update_layout(
    plot_bgcolor='#F1F1F1',  # Plot area background color
    paper_bgcolor='#F1F1F1',  # Overall figure background color
    font=dict(color="black"),  # Font color for labels and text
    )
    return(
        html.Div(
            [
                html.Div(
                    [
                        html.Button("5 Day" ,id={"type" : "graph-button", "index" : 2, "value" : "5d"}),
                        html.Button("1 Month" ,id={"type" : "graph-button", "index" : 3, "value" : "1mo"}),
                        html.Button("YTD" ,id={"type" : "graph-button", "index" : 4, "value" : "ytd"}),
                        html.Button("1 Year" ,id={"type" : "graph-button", "index" : 5, "value" : "1y"}),
                        html.Button("5 Years" ,id={"type" : "graph-button", "index" : 6, "value" : "5y"}),
                        html.Button("Max" ,id={"type" : "graph-button", "index" : 7, "value" : "max"}),
                        html.Button("Swap", id="swap-button" , n_clicks=0) 
                    ], className="flex px-8 justify-around", id="button-container"
                ),
                html.Div(
                    [
                    
                        dcc.Graph(figure=base_chart)

                    ], className="grow", id="graph-container"
                ),
            ], className="grow flex flex-col"
        )
      
        
    )
    