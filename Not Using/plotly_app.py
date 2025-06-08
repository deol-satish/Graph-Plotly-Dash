import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# --- Generate Sample Data ---
time = pd.date_range("2025-01-01", periods=100, freq="s")

# Placeholder for actual CSV loading:
utf_rtt_df = pd.read_csv('UDP-Prague.csv')
tfcubic_rtt_df = pd.read_csv('Cubic.csv')
baseline_rtt_df = pd.read_csv('Baseline_Propagation_Delay.csv')

# rtt_data = {
#     "UDP-Prague": np.random.uniform(5, 50, 100),
#     "Cubic": np.random.uniform(10, 60, 100),
#     "Baseline Propagation Delay": np.random.uniform(1, 10, 100)
# }


rtt_data = {
    "UDP-Prague": utf_rtt_df,
    "Cubic": tfcubic_rtt_df,
    "Baseline Propagation Delay": baseline_rtt_df
}


thrpt_data = {
    "UDP-Prague": np.random.uniform(40, 90, 100),
    "Cubic": np.random.uniform(30, 100, 100)
}

# --- Initialize Dash App ---
app = Dash(__name__)
server = app.server  # Needed for deployment

# --- Layout ---
app.layout = html.Div(style={'textAlign': 'center'}, children=[

    html.H1("RTT and Throughput Comparison"),

    # Dropdown to select metric
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'RTT', 'value': 'RTT'},
            {'label': 'Throughput', 'value': 'THRPT'}
        ],
        value='RTT',
        clearable=False,
        style={'width': '300px', 'margin': 'auto'}
    ),

    # Plot
    dcc.Graph(id='metric-graph'),

    # Demo video
    html.H2("Demo Video"),
    html.Video(
        controls=True,
        src="/static/input.mp4",
        style={"width": "640px", "height": "360px", "marginTop": "20px"}
    )
])

# --- Callback to update graph ---
@app.callback(
    Output('metric-graph', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_graph(metric):
    y_label = "RTT (ms)" if metric == "RTT" else "Throughput (Mbps)"
    title = "Smoothed RTT Over Time" if metric == "RTT" else "Throughput Over Time"
    data_dict = rtt_data if metric == "RTT" else thrpt_data

    traces = []
    for name, values in data_dict.items():
        traces.append(go.Scatter(
            x=time, y=values, mode='lines', name=name
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=y_label,
        hovermode='x unified'
    )
    return fig

# --- Run Server ---
if __name__ == '__main__':
    app.run(debug=True)
