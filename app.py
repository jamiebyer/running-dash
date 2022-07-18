
# visit http://127.0.0.1:8050/ in your web browser.

from os import environ

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
    external_stylesheets=external_stylesheets,
)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    """Running Dash"""
                ),
                dcc.Dropdown(
                    id="graph_type",
                    options=[
                        {'label': 'Speed vs. Time', 'value': 'speed'},
                        {'label': 'Map Position', 'value': 'map'},
                        {'label': 'Heart Rate vs. Time', 'value': 'hr'},
                        {'label': 'Elevation vs. Time', 'value': 'ele'},
                    ],
                    value='map'
                ),
                dcc.Graph(
                    id="graph"
                )
            ]
        )
    ],
)

data = pd.read_csv("data/running_data.csv")


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='graph_type', component_property='value')
)
def update_graph(graph_type):
    if graph_type == "speed":
        fig = px.line(data, x="times", y="lat", title='Lat vs. Time')
    elif graph_type == "map":
        fig = px.scatter_mapbox(data, lat="lat", lon="lon", mapbox_style="stamen-terrain", zoom=12)
        #fig = px.line(data, x="lat", y="lon")
    elif graph_type == "hr":
        fig = px.line(data, x="times", y="hr", title='Heart Rate vs. Time')
    elif graph_type == "ele":
        fig = px.line(data, x="times", y="ele", title='Elevation vs. Time')

    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
