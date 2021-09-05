# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import string

import pandas as pd
from scipy import signal
import numpy as np

from app_lib import alphabet

# Load stylesheet and create app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Basic data
letters = [{'label': x, 'value': x} for x in list(string.ascii_lowercase)]

# Create main layout sections
header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 75}),
            html.H3("Discrete Cosinus Transform", className="text-center")        ]
    ),
    className="mb-4",
)

control_panel = dbc.Card(
    [
        html.P("Choose your letter"),
        dcc.Dropdown(
            id='letters',
            options=letters,
            value='a'
        ),  
    ],
    className="shadow-sm bg-light p-4 mb-2",
    style={"minWidth": "250px"},
    id="filter-options",
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(control_panel, width=4),
                dbc.Col(
                    dcc.Graph(id='letter_display'),
                ),
                dbc.Col(
                    dash_table.DataTable(id='letter_table', style_header = {'display': 'none'})
                )
            ],
            className="m-2",
        ),

    ]
)

@app.callback(
    dash.dependencies.Output('letter_display', 'figure'),
    dash.dependencies.Output('letter_table', 'data'),
    dash.dependencies.Output('letter_table', 'columns'),
    dash.dependencies.Input('letters', 'value'),
)
def update_figure(value):
    list_letter = alphabet[value]
    letter = np.array([list(x) for x in list_letter]).astype(np.float)
    imgplot = px.imshow(letter, binary_string=True)

    letter_data_frame = pd.DataFrame(
        data=letter,
        columns = range(1,9),
        index = range(1,9)
    )
    letter_data_dict = letter_data_frame.to_dict('records')
    letter_columns = [{"name": str(i), "id": str(i)} for i in letter_data_frame.columns]

    return imgplot, letter_data_dict, letter_columns

if __name__ == '__main__':
    app.run_server(debug=True)