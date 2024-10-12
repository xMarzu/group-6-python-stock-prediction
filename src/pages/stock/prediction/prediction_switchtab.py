from src.pages.stock.prediction.prediction_info import predict_info_prophet,predict_info_linear
from src.pages.stock.prediction.start_predict_Linear import start_predict_Linear
from src.pages.stock.prediction.start_predict_Prophet import start_predict_Prophet
from linearRegression import validate_dates,validate_dates2
from dash import html, dcc, callback, Output, Input, State,dash_table
import plotly.graph_objs as go
import pandas as pd


def prediction_switchtab(formatted_date,tomorrow,years_before_10,years_before_4):
        return html.Div([
        dcc.Store(id='user-input-store-predict'),
        # Add Tabs for Linear and Prophet predictions
        dcc.Tabs(id='prediction-tabs', value='linear-tab', children=[
            dcc.Tab(label='Linear Regression', value='linear-tab', className="font-mono", children=[
                predict_info_linear(),
                dcc.Markdown(id='invalid',className="font-bold text-red-600 "),
                dcc.Markdown("**Start Date:**"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-start-linear',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    display_format='DD/MM/YYYY',
                    max_date_allowed=formatted_date,
                    date=years_before_10),
                dcc.Markdown("**End Date:**"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-end-linear',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    display_format='DD/MM/YYYY',
                    max_date_allowed=formatted_date,
                    date=formatted_date),
                html.Br(), 
                html.Button('Predict Next Day', id='predict-button-linear', n_clicks=0,className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
                dcc.Markdown(id='r2_score'),
                html.Br(),
                dcc.Markdown(id='r2_score2'),
            ]),
            dcc.Tab(label='Prophet Model', value='prophet-tab', className="font-mono", children=[
                predict_info_prophet(),
                dcc.Markdown("**Start Date:**"),
                dcc.Markdown(id='invalid2',className="font-bold text-red-600 "),
                dcc.DatePickerSingle(
                    id='prediction-date-input-start-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    display_format='DD/MM/YYYY',
                    max_date_allowed=formatted_date,
                    date=years_before_4),
                dcc.Markdown("**End Date:**"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-end-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    display_format='DD/MM/YYYY',
                    max_date_allowed=formatted_date,
                    date=formatted_date),
                dcc.Markdown("**Date you wish to predict:**"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-future-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    display_format='DD/MM/YYYY',
                    date=tomorrow),
                html.Br(), 
                html.Button('Predict Day', id='predict-button-prophet', n_clicks=0,className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
                dcc.Markdown(id='score_prophet'),
                html.Br(),
                dcc.Markdown(id='score_prophet2'),
                html.Br(),
                dash_table.DataTable(
                    id='prophet_metrics_table',
                    page_size=10,
                ),
                html.Br(),

            ]),
            
        ]),
        #A graph to display the data
        dcc.Graph(id='prediction-graph')
    ])


#Callback to store the state
@callback(
    Output('user-input-store-predict', 'data'),
    Input('prediction-date-input-start-linear', 'date'),
    Input('prediction-date-input-end-linear', 'date'),
    Input('prediction-date-input-start-prophet', 'date'),
    Input('prediction-date-input-end-prophet', 'date'),
    Input('prediction-date-input-future-prophet', 'date'),
)
#Store the user input
def store_user_inputs_predict(prediction_date_start_linear,prediction_date_end_linear, prediction_date_start_prophet,prediction_date_end_prophet,prediction_date_future_prophet):
    return {
        'prediction_date_start_linear': prediction_date_start_linear,
        'prediction_date_end_linear': prediction_date_end_linear,
        'prediction_date_start_prophet': prediction_date_start_prophet,
        'prediction_date_end_prophet': prediction_date_end_prophet,
        'prediction_date_future_prophet': prediction_date_future_prophet,

    }

#To pass everything back into the webpage
@callback(
    Output('prediction-graph', 'figure'),
    Output('r2_score','children'),
    Output('r2_score2','children'),
    Output('invalid','children'),
    Output('score_prophet','children'),
    Output('score_prophet2','children'),
    Output('invalid2','children'),
    Output('prophet_metrics_table','data'),
    Input('url', 'pathname'),
    Input('predict-button-linear', 'n_clicks'),
    Input('predict-button-prophet', 'n_clicks'),
    Input('prediction-tabs', 'value'),
    State('user-input-store-predict', 'data')
)
#Update the graph to display
def update_graph(pathname,n_clicks_linear,n_clicks_prophet,selected_tab,store_user_inputs_predict):
    # Extract stock_id from the URL
    stock_id = pathname.split('/')[-2] 
    
    #Empty List to make the display empty for the respective html id
    r2=[]
    prophet_score=[]
    invalid=[]
    invalid2=[]
    prophet_table=[]

    #When the page first loaded up
    if store_user_inputs_predict is None:
        return go.Figure(), r2,r2,invalid,prophet_score,prophet_score,invalid2,prophet_table
    
    #If linear tab is clicked
    elif selected_tab == 'linear-tab':
        #Get the input from the dates input
        start_date_str = store_user_inputs_predict['prediction_date_start_linear']
        end_date_str = store_user_inputs_predict['prediction_date_end_linear']
        #Change the inputs to datetime
        start_date = pd.to_datetime(start_date_str, errors='coerce')
        end_date = pd.to_datetime(end_date_str, errors='coerce')
        # Call the linear prediction function
        if n_clicks_linear > 0:
            if validate_dates(start_date, end_date):
                # If dates are valid, call the prediction function
                return start_predict_Linear(stock_id, start_date, end_date)
            else:
                # If dates are invalid, set the invalid message
                invalid = 'INVALID INPUT'
        else:
            #When the button is not clicked
            invalid= None    
    elif selected_tab == 'prophet-tab':
        #Get the input from the dates input
        start_date_str = store_user_inputs_predict['prediction_date_start_prophet']
        end_date_str = store_user_inputs_predict['prediction_date_end_prophet']
        predict_date_str=store_user_inputs_predict['prediction_date_future_prophet']
        #Change the inputs to datetime
        start_date = pd.to_datetime(start_date_str, errors='coerce')
        end_date = pd.to_datetime(end_date_str, errors='coerce')
        predict_date = pd.to_datetime(predict_date_str, errors='coerce')
        # Only call the Prophet prediction function if the button has been clicked
        if n_clicks_prophet > 0:
            if validate_dates2(start_date, end_date,predict_date):
                # If dates are valid, call the prediction function
                return start_predict_Prophet(stock_id, start_date, end_date, predict_date)
            else:
                # If dates are invalid, set the invalid message
                invalid2 = 'INVALID INPUT'
        else:
            # Handle the case when the button is not clicked
            invalid2 = None

    # Return the figure and any other output values
    return go.Figure(), r2,r2, invalid, prophet_score,prophet_score, invalid2,prophet_table