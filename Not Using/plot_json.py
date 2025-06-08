import json
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ---- Step 1: Load iperf3 JSON ----
with open("iperf3_client_cubic_iperf3_d120.json", "r") as f:
    data = json.load(f)

# ---- Step 2: Extract interval data ----
intervals = data.get("intervals", [])
records = []
for i, entry in enumerate(intervals):
    interval_data = entry.get("sum", {})
    records.append({
        "Interval": i,
        "Start": interval_data.get("start", 0),
        "End": interval_data.get("end", 0),
        "Throughput_Mbps": interval_data.get("bits_per_second", 0) / 1e6,
        "Retransmits": interval_data.get("retransmits", 0) if "retransmits" in interval_data else None,
    })

df = pd.DataFrame(records)

# ---- Step 3: Extract RTT (from final stream info) ----
rtt_ms = data.get("end", {}).get("streams", [{}])[0].get("sender", {}).get("rtt", 0) / 1000
df["RTT_ms"] = rtt_ms

# ---- Step 4: Create Dash App ----
app = dash.Dash(__name__)
app.title = "iPerf3 Metrics Dashboard"

app.layout = html.Div([
    html.H2("iPerf3 Server Metrics", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[
                {"label": "Throughput (Mbps)", "value": "Throughput_Mbps"},
                {"label": "Retransmissions", "value": "Retransmits"},
                {"label": "RTT (ms)", "value": "RTT_ms"},
            ],
            value="Throughput_Mbps",
            clearable=False,
            style={"width": "300px"}
        )
    ], style={"textAlign": "center", "marginBottom": "30px"}),

    dcc.Graph(id="metric-graph")
])

# ---- Step 5: Callback to update graph ----
@app.callback(
    Output("metric-graph", "figure"),
    Input("metric-dropdown", "value")
)
def update_graph(selected_metric):
    fig = px.line(
        df,
        x="Start",
        y=selected_metric,
        title=f"{selected_metric.replace('_', ' ')} over Time",
        markers=True
    )
    fig.update_layout(transition_duration=500, xaxis_title="Time (s)", yaxis_title=selected_metric.replace("_", " "))
    return fig

# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=True)
