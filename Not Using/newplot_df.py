import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Dummy data (replace with actual CSVs)
time = pd.date_range("2025-01-01", periods=100, freq="S")
tfcubic = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(30, 70, 100)})
utf = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(20, 60, 100)})
baseline_propagation_delay_df = pd.DataFrame({"Time": time, "SmoothedRTT": np.random.uniform(10, 50, 100)})

# Replace with real CSVs
# utf = pd.read_csv('UDP-Prague.csv')
# tfcubic = pd.read_csv('Cubic.csv')

baseline_Throuhgput_df = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(20, 80, 100)})
tfcubic_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(30, 100, 100)})
utf_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(40, 90, 100)})

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

app = dash.Dash(__name__)
app.title = "RTT and Throughput Comparison"

# ---- Layout ----
app.layout = html.Div([
    html.H2("Comparison of Smoothed RTT and Throughput", style={"textAlign": "center", "color": "white"}),

    html.Div([
        html.Label("Select Metric to Compare:", style={"color": "white"}),
        dcc.Dropdown(
            id="metric-type",
            options=[
                {"label": "Smoothed RTT", "value": "RTT"},
                {"label": "Throughput", "value": "THRPT"},
            ],
            value="RTT",
            clearable=False,
            style={"width": "300px", "margin": "auto"}
        )
    ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "marginBottom": "30px"}),

    dcc.Graph(id="comparison-graph")
], style={"backgroundColor": "#2c2c2c", "padding": "20px"})  # grey background

# ---- Callback ----
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
    fig.update_layout(
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font_color="white",
        xaxis_title="Time",
        yaxis_title=y_label.replace("thrpt", "Throughput (Mbps)").replace("SmoothedRTT", "RTT (ms)")
    )
    return fig

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True)
