import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# ---- Step 1: Load DataFrames ----
utf_rtt = pd.read_csv('./graph_data/udp_prague_rtt.csv')
tfcubic_rtt = pd.read_csv('./graph_data/cubic_rtt.csv')
baseline_propagation_delay_df = pd.read_csv('./graph_data/baseline_propagation_delay_df.csv')

baseline_throuhgput_df = pd.read_csv('./graph_data/baseline_throughput.csv')
tfcubic_thrpt = pd.read_csv('./graph_data/cubic_thrpt.csv')
utf_thrpt = pd.read_csv('./graph_data/udp_prague_thrpt.csv')

# ---- Step 2: Bundle data ----
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

dark_background = "#1e1e1e"
text_color = "#ffffff"
accent_color = "#0d6efd"

app.layout = html.Div(
    style={"backgroundColor": dark_background, "color": text_color, "padding": "20px"},
    children=[
        html.H2("Impact of L4S in Starlink Network - Smoothed RTT and Throughput", style={"textAlign": "center"}),

        dcc.Dropdown(
            id='metric-type',
            options=[
                {'label': 'RTT', 'value': 'RTT'},
                {'label': 'Throughput', 'value': 'Throughput (Mbit/s)'}
            ],
            value='RTT',
            clearable=False,
            style={
                'width': '300px',
                'margin': 'auto',
                'backgroundColor': "#f0f0f0",
                'color': "#0b0b0b",
                'border': '1px solid #444'
            }
        ),

        html.Div([
            dcc.Graph(
                id="comparison-graph",
                config={'displayModeBar': False},
                style={"width": "60%", "height": "100%"}
            ),
            html.Div([
                html.H4("Starlink Satellite Scenario Visualization", style={"textAlign": "center", "marginBottom": "10px"}),
                html.Video(
                    controls=True,
                    src="/static/starlink_viz_with_no_label.mp4",
                    style={"width": "100%", "height": "auto", "border": "1px solid #444"}
                )
            ], style={"width": "40%", "paddingLeft": "20px"})
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "marginTop": "30px"
        })
    ]
)


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
        y_label = "Throughput (Mbit/s)"
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
        markers=True,
        template="plotly_dark"
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=y_label.replace("Throughput (Mbit/s)", "Throughput (Mbps)").replace("SmoothedRTT", "RTT (ms)"),
        plot_bgcolor=dark_background,
        paper_bgcolor=dark_background,
        font=dict(color=text_color)
    )
    return fig

# ---- Step 5: Run ----
if __name__ == "__main__":
    app.run(debug=True)
