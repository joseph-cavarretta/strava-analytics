# visit http://0.0.0.0:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from charts import ChartHandler


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

path = '/app/data/processed/processed_activities_2024-08-12.csv'
#chart = ChartHandler()

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Chart-Title", id="card-title")
            #html.P("Description", id="card-description")
        ]
    )
)

app.layout = html.Div([
    dbc.Row([
        dbc.Col([card]), dbc.Col([card]), dbc.Col([card])
    ]),
    dbc.Row([
        dbc.Col([card]), dbc.Col([card]), dbc.Col([card])
    ]),
    dbc.Row([
        dbc.Col([card]), dbc.Col([card])
    ])
])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
