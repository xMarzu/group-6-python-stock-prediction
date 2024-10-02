import pandas as pd
import plotly.graph_objs as go
def generate_candlestick_chart(data):
    """Generate Candlestick Chart

    Args:
        data : Dataframe with stock data
    """
    data = pd.DataFrame.from_dict(data)
    print(data)
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
            open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'])
                    ]) 

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
    plot_bgcolor='#F1F1F1',  # Plot area background color
    paper_bgcolor='#F1F1F1',  # Overall figure background color
    font=dict(color="black"),  # Font color for labels and text
)
    return fig

