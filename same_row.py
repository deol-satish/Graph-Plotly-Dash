import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# ---- Step 1: Assume the following DataFrames are already defined ----
# Each DataFrame contains "Time" and either "SmoothedRTT" or "Throughput (Mbit/s)"

# Example dummy DataFrames (replace with your real ones)
# Replace these with: tfcubic, utf, baseline_propagation_delay_df, baseline_Throuhgput_df

utf_rtt = pd.read_csv('./graph_data/udp_prague_rtt.csv')
tfcubic_rtt = pd.read_csv('./graph_data/cubic_rtt.csv')
baseline_propagation_delay_df = pd.read_csv('./graph_data/baseline_propagation_delay_df.csv')

baseline_throuhgput_df = pd.read_csv('./graph_data/baseline_throughput.csv')
tfcubic_thrpt = pd.read_csv('./graph_data/cubic_thrpt.csv')
utf_thrpt = pd.read_csv('./graph_data/udp_prague_thrpt.csv')


tfcubic_loss = pd.read_csv('./graph_data/cubic_loss.csv')
utf_loss = pd.read_csv('./graph_data/udp_prague_loss.csv')


loss_paths = {
    "Cubic": tfcubic_loss,
    "UDP-Prague": utf_loss,
}

# ---- Step 2: Bundle data for RTT and throughput ----
rtt_paths = {
    "Cubic": tfcubic_rtt,
    "UDP-Prague": utf_rtt,
    "Baseline Propagation Delay": baseline_propagation_delay_df
}

thrpt_paths = {
    "Cubic": tfcubic_thrpt,
    "UDP-Prague": utf_thrpt,
    "Baseline Throughput": baseline_throuhgput_df
}

# ---- Step 3: Dash App ----
app = dash.Dash(__name__)
app.title = "RTT and Throughput Comparison"

app.layout = html.Div([
    html.H2("Impact of L4S in Starlink Network - Smoothed RTT and Throughput", style={"textAlign": "center"}),

    dcc.Dropdown(
        id='metric-type',
        options=[
            {'label': 'RTT', 'value': 'RTT'},
            {'label': 'Throughput', 'value': 'Throughput (Mbit/s)'}
        ],
        value='RTT',
        clearable=False,
        style={'width': '300px', 'margin': 'auto'}
    ),

    html.Div([
        dcc.Graph(id="comparison-graph", style={"width": "60%", "height": "100%"}),

        html.Div([
            html.H4("Starlink Satellite Scenario Visualization", style={"textAlign": "center"}),
            html.Video(
                controls=True,
                src="/static/starlink_viz_with_no_label.mp4",
                style={"width": "100%", "height": "auto"}
            )
        ], style={"width": "40%", "paddingLeft": "20px"})
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "marginTop": "30px"})
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
        title = "RTT Over Time"
    else:
        data_dict = thrpt_paths
        y_label = "Throughput (Mbit/s)"
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
    fig.update_layout(xaxis_title="Time", yaxis_title=y_label.replace("Throughput (Mbit/s)", "Throughput (Mbps)").replace("SmoothedRTT", "RTT (ms)"))
    return fig

# ---- Step 5: Run ----
if __name__ == "__main__":
    app.run(debug=True)
