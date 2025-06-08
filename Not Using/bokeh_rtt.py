import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource

# --- Step 1: Load or simulate data ---
utf = pd.read_csv('UDP-Prague.csv')
tfcubic = pd.read_csv('Cubic.csv')
baseline_propagation_delay_df = pd.read_csv('Baseline_Propagation_Delay.csv')

# Assuming 'Time' is in seconds, convert to datetime from Unix epoch (1970-01-01)
utf['Time'] = pd.to_datetime(utf['Time'], unit='s')
tfcubic['Time'] = pd.to_datetime(tfcubic['Time'], unit='s')
baseline_propagation_delay_df['Time'] = pd.to_datetime(baseline_propagation_delay_df['Time'], unit='s')

# --- Step 2: Prepare data for Bokeh ---
# Convert to Bokeh ColumnDataSource format for better compatibility
utf_source = ColumnDataSource(utf)
tfcubic_source = ColumnDataSource(tfcubic)
baseline_source = ColumnDataSource(baseline_propagation_delay_df)

# --- Step 3: Create a Bokeh plot ---
# Output file (you can change the path or output to a notebook if needed)
output_file("rtt_comparison_bokeh.html")

# Create a figure object with appropriate labels and title
p = figure(title="RTT Comparison across Different DataFrames", x_axis_label="Time", y_axis_label="Smoothed RTT", x_axis_type="datetime", width=800, height=400)

# Plot the lines for each dataset
p.line('Time (s)', 'SmoothedRTT', source=utf_source, legend_label='UDP-Prague', line_width=2, color="blue")
p.line('Time (s)', 'SmoothedRTT', source=tfcubic_source, legend_label='Cubic', line_width=2, color="green")
p.line('Time (s)', 'SmoothedRTT', source=baseline_source, legend_label='Baseline Propagation Delay', line_width=2, color="red")

# Customize the legend
p.legend.title = 'Legend'
p.legend.location = "top_left"

# Show the plot
show(p)
