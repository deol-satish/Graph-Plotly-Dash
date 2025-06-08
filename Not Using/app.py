import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select, HoverTool, Div
from bokeh.layouts import column, row, Spacer
from bokeh.palettes import Category10

# --- 1. Load or Simulate Data ---
# In a real scenario, you'd load your actual CSVs here.
# For demonstration, we'll continue with simulated data for throughput.
time_data = pd.date_range("2025-01-01", periods=100, freq="s")

# Placeholder for actual CSV loading:
# utf_rtt_df = pd.read_csv('UDP-Prague.csv')
# tfcubic_rtt_df = pd.read_csv('Cubic.csv')
# baseline_rtt_df = pd.read_csv('Baseline_Propagation_Delay.csv')

# Simulated RTT and Throughput dataframes (replace with your actual data)
# Assuming 'Time' column is already in a compatible format or can be converted.
utf_rtt_df = pd.DataFrame({"Time": time_data, "SmoothedRTT": np.random.uniform(10, 50, 100)})
tfcubic_rtt_df = pd.DataFrame({"Time": time_data, "SmoothedRTT": np.random.uniform(15, 60, 100)})
baseline_rtt_df = pd.DataFrame({"Time": time_data, "SmoothedRTT": np.random.uniform(5, 10, 100)})

utf_thrpt_df = pd.DataFrame({"Time": time_data, "thrpt": np.random.uniform(40, 90, 100)})
tfcubic_thrpt_df = pd.DataFrame({"Time": time_data, "thrpt": np.random.uniform(30, 100, 100)})

# --- 2. Organize Data Paths ---
data_sets = {
    "RTT": {
        "Cubic": tfcubic_rtt_df,
        "UDP-Prague": utf_rtt_df,
        "Baseline Propagation Delay": baseline_rtt_df
    },
    "THRPT": {
        "Cubic": tfcubic_thrpt_df,
        "UDP-Prague": utf_thrpt_df,
    }
}

# --- 3. Create Plot ---
plot = figure(
    x_axis_type="datetime",
    height=400,
    width=700,
    title="Data Over Time", # Initial generic title, updated by callback
    x_axis_label="Time"
)

hover = HoverTool(tooltips=[("Time", "@Time{%F %T}"), ("Value", "@y")], formatters={"@Time": "datetime"})
plot.add_tools(hover)

# --- 4. Setup Dropdown and Dynamic Plotting ---
metric_select = Select(title="Select Metric", value="RTT", options=["RTT", "THRPT"])
current_renderers = [] # To keep track of plotted lines for removal

def update_plot(attr, old, new):
    global current_renderers

    # Clear existing lines from the plot
    for r in current_renderers:
        plot.renderers.remove(r)
    current_renderers.clear()

    selected_metric = metric_select.value
    data_for_metric = data_sets[selected_metric]

    # Determine column name and labels based on selected metric
    y_column = "SmoothedRTT" if selected_metric == "RTT" else "thrpt"
    y_label = "RTT (ms)" if selected_metric == "RTT" else "Throughput (Mbps)"
    plot_title = "Smoothed RTT Over Time" if selected_metric == "RTT" else "Throughput Over Time"

    plot.yaxis.axis_label = y_label
    plot.title.text = plot_title
    plot.legend.items = [] # Clear existing legend items

    color_cycle = iter(Category10[10])

    for name, df in data_for_metric.items():
        color = next(color_cycle)
        # Ensure 'Time' is datetime for Bokeh plotting
        source_data = {
            "Time": pd.to_datetime(df['Time']),
            "y": df[y_column]
        }
        src = ColumnDataSource(data=source_data)
        line = plot.line("Time", "y", source=src, line_width=2, color=color, legend_label=name)
        current_renderers.append(line)

    plot.legend.title = "Legend"
    plot.legend.location = "top_center"

# --- Initial Plot Load and Callback Link ---
update_plot(None, None, None) # Call once to draw the initial plot
metric_select.on_change("value", update_plot)

# --- Layout ---
# Using Div for more precise centering control if needed, otherwise just row/column
# A simple column layout without Divs for centering is often sufficient and cleaner.
# If you want perfect center alignment, you might need to calculate widths or use CSS.
layout = column(
    row(Spacer(width=400), Div(text="<h1 style='text-align: center;'>TCP Metrics Dashboard</h1>"), Spacer(width=300)), # Center title
    row(Spacer(width=400), metric_select, Spacer(width=300)), # Adjust spacers to center
    row(Spacer(width=100), plot, Spacer(width=100)) # Adjust spacers to center
)

# --- Add to Document ---
curdoc().add_root(layout)
curdoc().title = "RTT and Throughput Comparison"