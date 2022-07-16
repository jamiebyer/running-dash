
# visit http://127.0.0.1:8050/ in your web browser.

from os import environ

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask

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
            ]
        )
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
