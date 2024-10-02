import plotly.express as px


def generate_line_chart(df):
    """Generates a line chart for stocks

    Args:
        df : Datframe 

    Returns:
        figure
    """
    fig = px.line(df, x="Date", y="Close")
    fig.update_layout(
    plot_bgcolor='#F1F1F1',  # Plot area background color
    paper_bgcolor='#F1F1F1',  # Overall figure background color
    font=dict(color="black"),  # Font color for labels and text
)
    return   (
        fig
    )
