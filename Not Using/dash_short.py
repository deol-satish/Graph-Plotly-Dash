import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Sample demo data
np.random.seed(42)
time = pd.date_range("2025-01-01", periods=100, freq="S")
data = pd.DataFrame({
    "Time": time,
    "Throughput": np.random.uniform(10, 50, size=100),
    "RTT": np.random.uniform(20, 100, size=100),
    "LossRate": np.random.uniform(0, 5, size=100)
})

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "TCP Metrics Dashboard"

# App layout
app.layout = html.Div([
    html.H1("TCP Metrics Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Metric:", style={"fontSize": "20px"}),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[
                {"label": "Throughput (Mbps)", "value": "Throughput"},
                {"label": "RTT (ms)", "value": "RTT"},
                {"label": "Loss Rate (%)", "value": "LossRate"},
            ],
            value="Throughput",
            clearable=False,
            style={"width": "300px"}
        )
    ], style={"textAlign": "center", "marginBottom": "30px"}),

    dcc.Graph(id="metric-graph")
])

# Callback to update graph
@app.callback(
    Output("metric-graph", "figure"),
    Input("metric-dropdown", "value")
)
def update_graph(selected_metric):
    fig = px.line(
        data,
        x="Time",
        y=selected_metric,
        title=f"{selected_metric} over Time",
        markers=True
    )
    fig.update_layout(transition_duration=500)
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
