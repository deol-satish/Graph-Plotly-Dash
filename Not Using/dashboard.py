import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. Generate Sample Data ---
# In a real-world scenario, you would load your data from a file or a database.
# Here, we'll create a pandas DataFrame with mock network performance data.

def generate_demo_data(num_points=100):
    """Creates a DataFrame with sample time-series network data."""
    base_time = datetime.now()
    timestamps = [base_time - timedelta(minutes=i) for i in range(num_points)]
    
    # Simulate realistic fluctuations
    throughput_data = [max(0, 800 + random.uniform(-200, 200) + i*0.5) for i in range(num_points)]
    rtt_data = [max(5, 30 + random.uniform(-15, 15) - i*0.1) for i in range(num_points)]
    loss_rate_data = [max(0, min(1, 0.02 + random.uniform(-0.015, 0.015))) for i in range(num_points)]
    
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Throughput (Mbps)': throughput_data,
        'RTT (ms)': rtt_data,
        'Loss Rate (%)': [x * 100 for x in loss_rate_data] # Convert to percentage
    })
    return df.sort_values('Timestamp').reset_index(drop=True)

df = generate_demo_data()

# --- 2. Initialize the Dash App ---
app = dash.Dash(__name__)
app.title = "Network Performance Dashboard"

# --- 3. Define the App Layout ---
# The layout is the structure of what the web application will look like.
# It uses Dash Core Components (dcc) and Dash HTML Components (html).

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    
    # Header
    html.H1(
        children='Network Performance Dashboard',
        style={
            'textAlign': 'center',
            'color': '#333'
        }
    ),

    # Description
    html.Div(
        children='Select a metric from the dropdown to visualize its performance over time.', 
        style={
            'textAlign': 'center',
            'color': '#666',
            'marginBottom': '30px'
        }
    ),

    # Dropdown for graph selection
    html.Div([
        html.Label('Select Metric:', style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Throughput', 'value': 'Throughput (Mbps)'},
                {'label': 'Round-Trip Time (RTT)', 'value': 'RTT (ms)'},
                {'label': 'Packet Loss Rate', 'value': 'Loss Rate (%)'}
            ],
            value='Throughput (Mbps)',  # Default value
            style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'middle'},
            clearable=False
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Graph component that will be updated by the callback
    dcc.Graph(
        id='performance-graph',
        config={'responsive': True} # Makes the graph responsive to window size
    )
])

# --- 4. Define the Callback ---
# Callbacks are the core of Dash interactivity.
# This function will be called whenever the input component's property changes
# (in this case, the 'value' of the 'metric-dropdown').

@app.callback(
    Output('performance-graph', 'figure'), # The component to update (the graph)
    [Input('metric-dropdown', 'value')]    # The component that triggers the update (the dropdown)
)
def update_graph(selected_metric):
    """
    This function updates the figure in the dcc.Graph component
    based on the dropdown selection.
    """
    # Create the plot using Plotly Express
    fig = px.line(
        df, 
        x='Timestamp', 
        y=selected_metric,
        title=f'{selected_metric} Over Time',
        markers=True,
        template='plotly_white' # Use a clean template
    )

    # Customize the layout for a more professional look
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title=selected_metric,
        title_font_size=24,
        title_x=0.5, # Center the title
        margin=dict(l=40, r=40, t=80, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#333'),
        xaxis=dict(gridcolor='#e9e9e9'),
        yaxis=dict(gridcolor='#e9e9e9')
    )
    
    # Add a subtle hover effect
    fig.update_traces(
        hovertemplate='<b>Timestamp</b>: %{x}<br><b>Value</b>: %{y:.2f}<extra></extra>'
    )

    return fig

# --- 5. Run the App ---
# This block allows you to run the app by executing the script from the command line.
if __name__ == '__main__':
    # To run this app:
    # 1. Save the code as a Python file (e.g., app.py).
    # 2. Open your terminal or command prompt.
    # 3. Navigate to the directory where you saved the file.
    # 4. Make sure you have the required libraries:
    #    pip install dash pandas plotly
    # 5. Run the script:
    #    python app.py
    # 6. Open a web browser and go to http://127.0.0.1:8050/
    
    app.run(debug=True)