import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from data import get_stock_data, generate_line_graph
import yfinance as yf
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go



dash.register_page(__name__, path_template="/stocks/<stock_id>")





def layout(stock_id=None, **kwargs):
    
    @callback(
        Output("stock-candlestick-graph","figure"),
         [
            Input("url","pathname"),
            
         ]
    )
    def request_candlestick_data(stock_id : str):
        stock_id = stock_id.split("/")[2]
        data = get_stock_data(stock_id, "10y")
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])
                     ]) 

        fig.update_layout(xaxis_rangeslider_visible=False)
        return fig
    
    @callback(
        [Output("stock-name","children"),
         Output("stock-line-graph", "figure")],
        [
            Input("url","pathname"),
            Input({'type':'line-button', 'index':ALL, 'value': ALL},"n_clicks"), 
          
             
        ]
       
    )
    def request_line_data(stock_id : str, buttons):
        triggered_id = ctx.triggered_id
        print(triggered_id)
    
        stock_id = stock_id.split("/")[2]
        data = []
        if (triggered_id == "url"):
            data = get_stock_data(stock_id, "10y")
        else:
            print(triggered_id["value"])
            data = get_stock_data(stock_id, triggered_id["value"])
        fig = generate_line_graph(data)
        selected_stock_message = f"The user requested stock ID: {stock_id}"
        return selected_stock_message,fig

    # @callback(
    #     Output("stock-line-graph","figure"),
    #     [Input("1d-button","value"), 
    #      Input("5d-button","value"), 
    #      Input("1m-button","value"), 
    #      Input("ytd-button","value"), 
    #      Input("1y-button","value"), 
    #      Input("5y-button","value"), 
    #      Input("10y-button","value"),
    #      Input("url","pathname")]
    # )
    # def update_line_period(date_value : str, stock_id : str):
    #     stock_id = stock_id.split("/")[2]
    #     data = get_stock_data(stock_id, date_value)
    #     fig = generate_line_graph(data)
    #     return fig
        


    return html.Div(
        
        [
            dcc.Location(id='url'),
            html.H1( children=[] ,id="stock-name"),
            html.Div(
                [
                    html.Div(
                        [
                            dbc.Button(children=["1 Day"], color="light", class_name="me-1", value="1d", id={"type" : "line-button", "index" : 1, "value": "1d"}),
                            dbc.Button(children=["5 Days"], color="light", class_name="me-1", value="5d",  id={"type" : "line-button", "index" : 2, "value": "5d"}),   
                            dbc.Button(children=["1 Month"], color="light", class_name="me-1", value="1mo", id={"type" : "line-button", "index" : 3, "value": "1mo"}),   
                            dbc.Button(children=["YTD"], color="light", class_name="me-1", value="ytd", id={"type" : "line-button", "index" : 4, "value": "ytd"}),
                            dbc.Button(children=["1 Year"], color="light", class_name="me-1",value="1y", id={"type" : "line-button", "index" : 5, "value": "1y"}),
                            dbc.Button(children=["5 Years"], color="light", class_name="me-1", value="5y", id={"type" : "line-button", "index" : 6, "value": "5y"}),
                            dbc.Button(children=["10 Years"], color="light", class_name="me-1", value="10y", id={"type" : "linebutton", "index" : 7, "value": "10y"}),
                             
                        ]
                    ),
                      dcc.Graph(figure={}, id="stock-line-graph" , config={"displayModeBar" : False}),
                ]
               
            ),
            html.Div(
                [
                    dcc.Graph(figure={}, id="stock-candlestick-graph")
                ]
            )
           
        ]
        
    )