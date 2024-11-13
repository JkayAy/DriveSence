"""This script defines the layout for the Dash frontend, which includes a title, a dropdown for filtering violation types (with options like "All" or "Speed Violation"), and a map visualization to display vehicle violations. It also includes a data table that shows detailed information about each violation, such as license plate, speed, latitude, longitude, and timestamp, with pagination set to display 10 records per page. The map and table are connected to the backend data and dynamically updated based on user input."""

# frontend/layout.py
from dash import dcc
from dash import html
from dash import dash_table
from dash import dash_table

layout = html.Div([
    html.H1("Vehicle Violation Dashboard"),
    
    # Dropdown or filter section if needed
    dcc.Dropdown(
        id='violation-filter',
        options=[
            {'label': 'All', 'value': 'ALL'},
            {'label': 'Speed Violation', 'value': 'SPEED'},
        ],
        value='ALL',
        clearable=False,
    ),
    
    # Map Section to show violations on map
    dcc.Graph(id='map-visualization'),

    # Table to show the violation list
    dash_table.DataTable(
        id='violation-table',
        columns=[
            {"name": "License Plate", "id": "license_plate"},
            {"name": "Speed", "id": "speed"},
            {"name": "Latitude", "id": "latitude"},
            {"name": "Longitude", "id": "longitude"},
            {"name": "Timestamp", "id": "timestamp"}
        ],
        page_size=10
    ),
])
