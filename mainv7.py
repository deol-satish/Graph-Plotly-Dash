import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# ---- Load CSVs ----
utf_rtt = pd.read_csv('./graph_data/udp_prague_rtt.csv')
tfcubic_rtt = pd.read_csv('./graph_data/cubic_rtt.csv')
baseline_propagation_delay_df = pd.read_csv('./graph_data/baseline_propagation_delay_df.csv')

baseline_throuhgput_df = pd.read_csv('./graph_data/baseline_thrpt.csv')
tfcubic_thrpt = pd.read_csv('./graph_data/cubic_thrpt.csv')
utf_thrpt = pd.read_csv('./graph_data/udp_prague_thrpt.csv')

tfcubic_loss = pd.read_csv('./graph_data/cubic_loss.csv')
utf_loss = pd.read_csv('./graph_data/udp_prague_loss.csv')

# ---- Bundle Data ----
rtt_paths = {
    "CUBIC": tfcubic_rtt,
    "L4S": utf_rtt,
    "Propagation Delay": baseline_propagation_delay_df
}
thrpt_paths = {
    "CUBIC": tfcubic_thrpt,
    "L4S": utf_thrpt,
    "Bandwidth": baseline_throuhgput_df
}
loss_paths = {
    "CUBIC": tfcubic_loss,
    "L4S": utf_loss,
}

# ---- Utility: Combine Data ----
def prepare_graph_data(data_dict, y_label, label_fallback=0):
    combined = []
    for name, df in data_dict.items():
        df_copy = df.copy()
        if y_label not in df_copy.columns:
            df_copy[y_label] = label_fallback
        combined.append(df_copy[["Time", y_label]].assign(Legend=name))
    return pd.concat(combined)

# ---- Prepare Figures ----
rtt_fig = px.line(
    prepare_graph_data(rtt_paths, "SmoothedRTT"),
    x="Time", y="SmoothedRTT", color="Legend"
)
rtt_fig.update_layout(
    title="",
    xaxis_title="Time (s)",
    yaxis_title="Round-Trip Time (ms)"
)

thrpt_fig = px.line(
    prepare_graph_data(thrpt_paths, "Throughput (Mbit/s)"),
    x="Time", y="Throughput (Mbit/s)", color="Legend"
)
thrpt_fig.update_layout(
    title="",
    xaxis_title="Time (s)",
    yaxis_title="Throughput (Mbps)"
)

loss_fig = px.line(
    prepare_graph_data(loss_paths, "Loss"),
    x="Time", y="Loss", color="Legend"
)
loss_fig.update_layout(
    title="",
    xaxis_title="Time (s)",
    yaxis_title="Packet Loss"
)

# ---- Dash App Layout ----
app = dash.Dash(__name__)
app.title = "L4S - Starlink Impact Visualization"

demo_title = "Network Telemetry Visualization for Low Latency, Low Loss, Scalable Throughput (L4S) over Starlink Network"

common_style = {
    "height": "500px",
    "boxSizing": "border-box",
    "backgroundColor": "#ffffff",
    "borderRadius": "10px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
    "padding": "10px",
    "overflow": "hidden"
}

common_style = {
    "height": "500px",
    "boxSizing": "border-box",
    "backgroundColor": "#ffffff",
    "borderRadius": "10px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
    "padding": "10px",
    "overflow": "hidden"
}

header_style = {
    "textAlign": "center",
    "color": "white",
    "backgroundColor": "#3498db",
    "padding": "12px",
    "borderRadius": "8px",
    "fontWeight": "bold",
    "fontSize": "18px",
    "marginBottom": "10px"
}

app.layout = html.Div([
    html.Div([
        html.H2(
            demo_title,
            style={"textAlign": "center", "color": "white", "margin": "0"}
        )
    ], style={
        "backgroundColor": "#2c3e50",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
        "marginBottom": "20px"
    }),

    html.Div([  # First Row: Throughput + Simulation
        html.Div([
            html.Div("Throughput (Mbit/s) vs Time", style=header_style),
            dcc.Graph(figure=thrpt_fig, style={"height": "420px"})
        ], style={**common_style, "width": "50%", "marginRight": "2%"}),

        html.Div([
            html.Div("Starlink Constellation Simulation", style=header_style),
            html.Video(
                controls=True,
                src="/static/starlink_viz_with_no_label.mp4",
                style={"width": "100%", "height": "420px", "borderRadius": "8px"}
            )
        ], style={**common_style, "width": "48%"})
    ], style={"display": "flex", "marginBottom": "30px"}),

    html.Div([  # Second Row: RTT + Packet Loss
        html.Div([
            html.Div("RTT (ms) vs Time", style=header_style),
            dcc.Graph(figure=rtt_fig, style={"height": "420px"})
        ], style={**common_style, "width": "50%", "marginRight": "2%"}),

        html.Div([
            html.Div("Packet Loss vs Time", style=header_style),
            dcc.Graph(figure=loss_fig, style={"height": "420px"})
        ], style={**common_style, "width": "48%"})
    ], style={"display": "flex", "marginBottom": "30px"})
], style={
    "fontFamily": "Segoe UI, sans-serif",
    "padding": "30px",
    "backgroundColor": "#f7f9fb",
    "minHeight": "100vh"
})




# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=True)
