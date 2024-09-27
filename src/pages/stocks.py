import dash
from dash import html
import dash_bootstrap_components as dbc

##stocks page
dash.register_page(__name__, )

layout = html.Div([
    html.H1('This is our Stocks page'),
    html.Div('This is our Stocks page content.'),
    html.A(
        
        children=[
            dbc.Button("AAPL", color="primary", class_name="mx-1")
        ],
        href="/stocks/AAPL"
    ),
      html.A(
        
        children=[
            dbc.Button("AAPL", color="primary", class_name="mx-1")
        ],
        href="/stocks/AAPL"
    ),
      html.A(
        
        children=[
            dbc.Button("AAPL", color="primary", class_name="mx-1")
        ],
        href="/stocks/AAPL"
    ),

  
])