import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select, Legend, Div
from bokeh.layouts import column, row, Spacer
from bokeh.palettes import Category10
from bokeh.models import HoverTool

# --- Step 1: Load or simulate data ---
time = pd.date_range("2025-01-01", periods=100, freq="s")

# Replace these with real CSVs
# Make sure 'UDP-Prague.csv', 'Cubic.csv', and 'Baseline_Propagation_Delay.csv' exist
# For demonstration, I'll create dummy CSVs if they don't exist
try:
    utf = pd.read_csv('UDP-Prague.csv')
except FileNotFoundError:
    print("UDP-Prague.csv not found, creating dummy data.")
    utf = pd.DataFrame({"Time": np.arange(100), "SmoothedRTT": np.random.uniform(5, 50, 100)})

try:
    tfcubic = pd.read_csv('Cubic.csv')
except FileNotFoundError:
    print("Cubic.csv not found, creating dummy data.")
    tfcubic = pd.DataFrame({"Time": np.arange(100), "SmoothedRTT": np.random.uniform(10, 60, 100)})

try:
    baseline_propagation_delay_df = pd.read_csv('Baseline_Propagation_Delay.csv')
except FileNotFoundError:
    print("Baseline_Propagation_Delay.csv not found, creating dummy data.")
    baseline_propagation_delay_df = pd.DataFrame({"Time": np.arange(100), "SmoothedRTT": np.random.uniform(1, 10, 100)})


# Simulated throughput for example
utf_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(40, 90, 100)})
tfcubic_thrpt = pd.DataFrame({"Time": time, "thrpt": np.random.uniform(30, 100, 100)})

# Step 2: Prepare dictionary for access
rtt_paths = {
    "Cubic": tfcubic,
    "UDP-Prague": utf,
    "Baseline Propagation Delay": baseline_propagation_delay_df
}

thrpt_paths = {
    "Cubic": tfcubic_thrpt,
    "UDP-Prague": utf_thrpt,
}

# --- Step 3: Create figure ---
plot = figure(x_axis_type="datetime", title="Smoothed RTT Over Time", height=400, width=700)
plot.xaxis.axis_label = "Time"
plot.yaxis.axis_label = "RTT (ms)"

hover = HoverTool()
hover.tooltips = [("Time", "@Time{%F %T}"), ("Value", "@y")]
hover.formatters = {"@Time": "datetime"}
plot.add_tools(hover)

# --- Step 4: Setup dropdown and source ---
metric_select = Select(title="Select Metric", value="RTT", options=["RTT", "THRPT"])
data_sources = {}
renderers = []

def update_plot(attr, old, new):
    global renderers
    # Remove previous renderers
    for r in renderers:
        plot.renderers.remove(r)
    renderers.clear()

    metric = metric_select.value
    data_dict = rtt_paths if metric == "RTT" else thrpt_paths
    y_col = "SmoothedRTT" if metric == "RTT" else "thrpt"
    ylabel = "RTT (ms)" if metric == "RTT" else "Throughput (Mbps)"
    title = "Smoothed RTT Over Time" if metric == "RTT" else "Throughput Over Time"

    plot.yaxis.axis_label = ylabel
    plot.title.text = title

    color_cycle = iter(Category10[10])
    legend_items = []

    for name, df in data_dict.items():
        color = next(color_cycle)
        src = ColumnDataSource(data={
            "Time": pd.to_datetime(df['Time'], unit='s'),
            "y": df[y_col]
        })
        line = plot.line("Time", "y", source=src, line_width=2, color=color, legend_label=name)
        renderers.append(line)

    plot.legend.title = "Legend"
    plot.legend.location = "top_center"

# --- Initial load ---
update_plot(None, None, None)

# --- Link callback ---
metric_select.on_change("value", update_plot)

# --- Add the video demo ---
from bokeh.models import Div

video_html = """
<div style="text-align: center; margin-top: 20px;">
    <h2>Demo Video</h2>
    <video width="640" height="360" controls>
        <source src="input.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>
"""

video_div = Div(text=video_html)


# --- Centering the plot and dropdown ---
plot_layout = column(Spacer(height=60), plot, Spacer(height=60))
dropdown_layout = column(Spacer(width=60,height=60), metric_select, Spacer(height=60))

# --- Create a Div for center-aligned layout ---
# Combine the dropdown, plot, and video
content_column = column(dropdown_layout, plot_layout, video_div) # Add video_div here

final_layout = row(
    Spacer(width=400),  # Spacer to center the content horizontally
    content_column
)

# --- Add to document ---
curdoc().add_root(final_layout)
curdoc().title = "RTT and Throughput Comparison"