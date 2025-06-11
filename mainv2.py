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

baseline_throuhgput_df = pd.read_csv('./graph_data/baseline_thrpt.csv')
tfcubic_thrpt = pd.read_csv('./graph_data/cubic_thrpt.csv')
utf_thrpt = pd.read_csv('./graph_data/udp_prague_thrpt.csv')

tfcubic_loss = pd.read_csv('./graph_data/cubic_loss.csv')
utf_loss = pd.read_csv('./graph_data/udp_prague_loss.csv')


# ---- Step 2: Bundle data for RTT, throughput, and loss ----
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

loss_paths = {
    "Cubic": tfcubic_loss,
    "UDP-Prague": utf_loss,
}


# ---- Step 3: Dash App ----
app = dash.Dash(__name__)
app.title = "RTT, Throughput, and Packet Loss Comparison"

# app.layout = html.Div([
#     html.H2("Impact of L4S in Starlink Network - Smoothed RTT, Throughput, and Packet Loss", style={"textAlign": "center"}),

#     dcc.Dropdown(
#         id='metric-type',
#         options=[
#             {'label': 'RTT', 'value': 'RTT'},
#             {'label': 'Throughput', 'value': 'Throughput (Mbit/s)'},
#             {'label': 'Packet Loss', 'value': 'Lost_Packets'} # Added Loss option
#         ],
#         value='RTT',
#         clearable=False,
#         style={'width': '300px', 'margin': 'auto'}
#     ),

#     html.Div([
#         dcc.Graph(id="comparison-graph", style={"width": "60%", "height": "100%"}),

#         html.Div([
#             html.H4("Starlink Satellite Scenario Visualization", style={"textAlign": "center"}),
#             html.Video(
#                 controls=True,
#                 src="/static/starlink_viz.mp4",
#                 style={"width": "100%", "height": "auto"}
#             )
#         ], style={"width": "40%", "paddingLeft": "20px"})
#     ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "marginTop": "30px"})
# ])


app.layout = html.Div([
    # Title Card
    html.Div([
        html.H2(
            "Impact of L4S in Starlink Network - Smoothed RTT, Throughput, and Packet Loss",
            style={"textAlign": "center", "color": "white", "margin": "0"}
        )
    ], style={
        "backgroundColor": "#2c3e50",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
        "marginBottom": "20px"
    }),

    # Dropdown Container
    html.Div([
        dcc.Dropdown(
            id='metric-type',
            options=[
                {'label': 'RTT', 'value': 'RTT'},
                {'label': 'Throughput', 'value': 'Throughput (Mbit/s)'},
                {'label': 'Packet Loss', 'value': 'Lost_Packets'}
            ],
            value='RTT',
            clearable=False,
            style={'width': '300px', 'margin': '0 auto'}
        )
    ], style={
        "backgroundColor": "#ecf0f1",
        "padding": "15px",
        "borderRadius": "10px",
        "margin": "0 auto 20px auto",
        "width": "fit-content",
        "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.1)"
    }),

    # Graph + Video Container
    html.Div([
        # Graph Box
        html.Div([
            dcc.Graph(id="comparison-graph", style={"height": "500px"})
        ], style={
            "backgroundColor": "#ffffff",
            "padding": "5px",
            "borderRadius": "5px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "width": "70%",
            "marginRight": "5px"
        }),

        # Video Box
        html.Div([
            html.H4("Starlink Satellite Scenario Visualization", style={"textAlign": "center", "marginBottom": "10px"}),
            html.Video(
                controls=True,
                src="/static/starlink_viz.mp4",
                style={"width": "100%", "height": "auto", "borderRadius": "8px"}
            )
        ], style={
            "backgroundColor": "#f2f3f4",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "width": "40%"
        })
    ], style={
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "flex-start",
        "marginTop": "30px",
        "gap": "20px"
    })
], style={
    "fontFamily": "Segoe UI, sans-serif",
    "padding": "30px",
    "backgroundColor": "#f7f9fb",
    "minHeight": "100vh"
})



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
        y_axis_title = "RTT (ms)"
    elif metric_type == "Throughput (Mbit/s)":
        data_dict = thrpt_paths
        y_label = "Throughput (Mbit/s)"
        title = "Throughput Over Time"
        y_axis_title = "Throughput (Mbps)"
    elif metric_type == "Lost_Packets": # New condition for Loss
        data_dict = loss_paths
        y_label = "Loss" # Assuming the column name for loss is "Loss"
        title = "Packet Loss Over Time"
        y_axis_title = "Packet Loss"

    # Combine data into one DataFrame with "Variant" column
    # Ensure that `y_label` exists in the dataframes, otherwise assign a dummy column if not present.
    combined_data_frames = []
    for name, df in data_dict.items():
        if y_label not in df.columns:
            # If the y_label column is not present, add a dummy column
            # This handles cases where dataframes might not have all metric columns
            # For a real application, ensure your CSVs have consistent column names
            df_copy = df.copy()
            df_copy[y_label] = 0 # Placeholder: consider how to handle missing data appropriately
            combined_data_frames.append(df_copy[["Time", y_label]].assign(Variant=name))
        else:
            combined_data_frames.append(df[["Time", y_label]].assign(Variant=name))

    combined = pd.concat(combined_data_frames)

    fig = px.line(
        combined,
        x="Time",
        y=y_label,
        color="Variant",
        title=title,
        markers=True
    )
    fig.update_layout(xaxis_title="Time", yaxis_title=y_axis_title)
    return fig

# ---- Step 5: Run ----
if __name__ == "__main__":
    app.run(debug=True)