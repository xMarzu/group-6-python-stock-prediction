
import dash
from dash import html, dcc
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from dash import dash_table
from src.components.home.home_search_bar import home_search_bar
from constants import STOCK_LIST
from src.components.home.top_gainer_loser import generate_top_loser_gainer
dash.register_page(__name__, path='/')




layout = html.Div([
    html.Div(
        [
            html.P("Welcome to Stonks Analysis", className="font-mono text-5xl font-bold"),
            html.P("Search for your favourite stocks below here"),
            home_search_bar(),    
            generate_top_loser_gainer()   
            
        ], className="text-3xl  flex flex-col items-center justify-center text-center gap-4"
    )
    
], className="")