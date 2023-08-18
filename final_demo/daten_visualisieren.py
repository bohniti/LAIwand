import plotly.express as px

def generate_plotly_plot(df):
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
    return fig
