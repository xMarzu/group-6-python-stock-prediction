from dash import html, dcc, callback, Output, Input, State

def predict_info_linear():
    return(
        html.Div([
            html.H3("This prediction tool utilizes Linear Regression to forecast stock prices."),
            html.H3("To begin, please enter a start date and an end date for the model's training."),
            html.H3("After clicking the 'Predict Next Day' button, you will receive the predicted stock price for the following day, along with the R-squared score that indicates the model's performance."),
            dcc.Markdown("**Note that the model requires at least one month of data to function properly.**")
        ])
    )

def predict_info_prophet():
    return(
        html.Div([
            html.H3("This prediction tool utilizes Prophet Model to forecast stock prices."),
                html.H3("To begin, please enter a start date and an end date for the model's training."),
                html.H3("Please also enter a date that you wish to predict."),
                html.H3("After clicking the 'Predict Day' button, you will receive the predicted stock price for the specificed day."),
                dcc.Markdown("**Note that the model requires at least one month of data to function properly.**"),
        ])
    )