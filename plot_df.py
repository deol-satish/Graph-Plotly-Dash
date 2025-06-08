import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# ---- Step 1: Assume the following DataFrames are already defined ----
# Each DataFrame contains "Time" and either "SmoothedRTT" or "thrpt"

# Example dummy DataFrames (replace with your real ones)
# Replace these with: tfcubic, utf, baseline_propagation_delay_df, baseline_Throuhgput_df
time = pd.date_range("2025-01-01", periods=100, freq="S")
tfcubic = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(30, 70, 100)})
utf = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(20, 60, 100)})
baseline_propagation_delay_df = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(10, 50, 100)})

utf = pd.read_csv('UDP-Prague.csv')
tfcubic = pd.read_csv('Cubic.csv')
baseline_propagation_delay_df = pd.read_csv('Baseline_Propagation_Delay.csv')

baseline_Throuhgput_df = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(20, 80, 100)})
tfcubic_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(30, 100, 100)})
utf_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(40, 90, 100)})


# ---- Step 2: Bundle data for RTT and throughput ----
rtt_paths = {
    "Cubic": tfcubic,
    "UDP-Prague": utf,
    # "Baseline Propagation Delay": baseline_propagation_delay_df
}

thrpt_paths = {
    "Cubic": tfcubic_thrpt,
    "UDP-Prague": utf_thrpt,
    # "Baseline Throughput": baseline_Throuhgput_df
}

# ---- Step 3: Dash App ----
app = dash.Dash(__name__)
app.title = "RTT and Throughput Comparison"

app.layout = html.Div([
    html.H2("Comparison of Smoothed RTT and Throughput", style={"textAlign": "center"}),

    # html.Div([
    #     html.Label("Select Metric to Compare:"),
    #     dcc.Dropdown(
    #         id="metric-type",
    #         options=[
    #             {"label": "Smoothed RTT", "value": "RTT"},
    #             {"label": "Throughput", "value": "THRPT"},
    #         ],
    #         value="RTT",
    #         clearable=False,
    #         style={"width": "300px", "margin": "auto"}
    #     )
    # ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Dropdown to select metric
    dcc.Dropdown(
        id='metric-type',
        options=[
            {'label': 'RTT', 'value': 'RTT'},
            {'label': 'Throughput', 'value': 'THRPT'}
        ],
        value='RTT',
        clearable=False,
        style={'width': '300px', 'margin': 'auto'}
    ),

    dcc.Graph(id="comparison-graph"),

    html.H2("Starlink Satellite Scenario Visualization", style={"textAlign": "center", "marginTop": "10px"}),

    html.Div([
        html.Video(
            controls=True,
            src="/static/input.mp4",
            style={"width": "854px", "height": "480px"}
        )
    ], style={"textAlign": "center", "marginTop": "10px"})
])


# ---- Step 4: Callback ----
@app.callback(
    Output("comparison-graph", "figure"),
    Input("metric-type", "value")
)
def update_comparison_graph(metric_type):
    if metric_type == "RTT":
        data_dict = rtt_paths
        y_label = "SmoothedRTT"
        title = "Smoothed RTT Over Time"
    else:
        data_dict = thrpt_paths
        y_label = "thrpt"
        title = "Throughput Over Time"

    # Combine data into one DataFrame with "Variant" column
    combined = pd.concat([
        df[["Time", y_label]].assign(Variant=name)
        for name, df in data_dict.items()
    ])

    fig = px.line(
        combined,
        x="Time",
        y=y_label,
        color="Variant",
        title=title,
        markers=True
    )
    fig.update_layout(xaxis_title="Time", yaxis_title=y_label.replace("thrpt", "Throughput (Mbps)").replace("SmoothedRTT", "RTT (ms)"))
    return fig

# ---- Step 5: Run ----
if __name__ == "__main__":
    app.run(debug=True)
