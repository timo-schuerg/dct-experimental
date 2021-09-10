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
from scipy.fftpack import dct, idct
import numpy as np

from app_lib import alphabet

# Helper functions for 2d-discrete cosine transform
def dct2(a):
    return dct(dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(a):
    return idct(idct(a, axis=0 , norm='ortho'), axis=1 , norm='ortho')

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

control_letter = dbc.Card(
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
    id="filter-letter-options",
)
control_cutoff = dbc.Card(
    [
        html.P("Choose your cutoff"),
        dcc.Slider(
            id='cutoff',
            min=0,
            max=1,
            step=0.01,
            value=0,
            marks={ np.round(i,2): str(np.round(i,2)) for i in np.linspace(0,1,10,endpoint=False).tolist()}
        ), 
    ],
    className="shadow-sm bg-light p-4 mb-2",
    style={"minWidth": "250px"},
    id="filter-cutoff",
)
letter_display = dbc.Card(
    [
        html.P("Your choice as graphic:"),
        dcc.Graph(id='letter_display'),
    ],
    className="p-4 mr-2 shadow-sm bg-light",
)
phase_display = dbc.Card(
    [
        html.P("Your letter after transformation:"),
        dcc.Graph(id='phase_display'),
    ],
    className="p-4 mr-2 shadow-sm bg-light",
)
quant_display = dbc.Card(
    [
        html.P("Your letter after transformation and quantization:"),
        dcc.Graph(id='quant_display'),
    ],
    className="p-4 mr-2 shadow-sm bg-light",
)
letter_matrix_display = dbc.Card(
    [
        html.P("Your choice as matrix:"),
        dash_table.DataTable(id='letter_table', style_header = {'display': 'none'})
    ],
    className="p-4 mr-2 shadow-sm bg-light",
)
phase_matrix_display = dbc.Card(
    [
        html.P("The transformed image as matrix:"),
        dash_table.DataTable(id='phase_table', style_header = {'display': 'none'})
    ],
    className="p-4 mr-2 shadow-sm bg-light",
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(html.Div("First choose your input"), width=4)
            ],
            justify="start"
        ),
        dbc.Row(
            [
                dbc.Col(control_letter, width=4),
                dbc.Col(letter_display, width=4),
                dbc.Col(letter_matrix_display, width=4)
            ],
            className="m-2",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("Your input in phase space"), width=4)
            ],
            justify="start"
        ),
         dbc.Row(
            [
                dbc.Col(phase_display, width=4),
                dbc.Col(phase_matrix_display, width=4)
            ],
            justify="end",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("Your input after quantization"), width=4)
            ],
            justify="start"
        ),
        dbc.Row(
            [
                dbc.Col(control_cutoff, width=4),
                dbc.Col(quant_display, width=4),
                dbc.Col(
                    dbc.Card(
                        [html.H6(id="compression_rate"), html.P("Compression rate")],
                        className="p-4 mr-2 shadow-sm bg-light",
                        id="compression",
                    ),
                    width=4
                )
            ]
        )
    ],
    fluid=True,
    className="bg-light",
)

@app.callback(
    dash.dependencies.Output('letter_display', 'figure'),
    dash.dependencies.Output('letter_table', 'data'),
    dash.dependencies.Output('letter_table', 'columns'),
    dash.dependencies.Output('quant_display', 'figure'),
    dash.dependencies.Output('compression_rate', 'children'),
    dash.dependencies.Output('phase_display', 'figure'),
    dash.dependencies.Output('phase_table', 'data'),
    dash.dependencies.Output('phase_table', 'columns'),
    dash.dependencies.Input('letters', 'value'),
    dash.dependencies.Input('cutoff', 'value'),
)
def update_figure(letters, cutoff):

    # Load letter and convert to numpy array
    list_letter = alphabet[letters]
    letter = np.array([list(x) for x in list_letter]).astype(np.float)

    # Create plot of letter
    imgplot = px.imshow(
        letter,
        binary_string=True,
        width=256,
        height=256
    )
    imgplot.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, b=10, t=10)
    )
    imgplot.update_xaxes(showticklabels=False)
    imgplot.update_yaxes(showticklabels=False)

    # Create matrix view of letter
    letter_data_frame = pd.DataFrame(
        data=letter,
        columns = range(1,9),
        index = range(1,9)
    )
    letter_data_dict = letter_data_frame.to_dict('records')
    letter_columns = [{"name": str(i), "id": str(i)} for i in letter_data_frame.columns]

    # Create image of transformed letter
    letter_trans = dct2(letter)
    transplot = px.imshow(
        letter_trans,
        binary_string=True,
        width=256,
        height=256
    )
    transplot.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, b=10, t=10)
    )
    transplot.update_xaxes(showticklabels=False)
    transplot.update_yaxes(showticklabels=False)

    # Create matrix view of transformed letter
    trans_letter_data_frame = pd.DataFrame(
        data=letter_trans.round(2),
        columns = range(1,9),
        index = range(1,9)
    )
    trans_letter_data_dict = trans_letter_data_frame.to_dict('records')
    trans_letter_columns = [{"name": str(i), "id": str(i)} for i in trans_letter_data_frame.columns]

    # Create image of transformed and cut off letter
    quant = letter_trans.copy()
    quant[np.absolute(quant) < cutoff]=0
    quantplot = px.imshow(
        idct2(quant),
        binary_string=True,
        width=256,
        height=256
    )
    quantplot.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, b=10, t=10)
    )
    quantplot.update_xaxes(showticklabels=False)
    quantplot.update_yaxes(showticklabels=False)

    # Compute compression rate
    compression_rate =  64 / (quant > 0).sum()

    return imgplot, letter_data_dict, letter_columns, quantplot, compression_rate, transplot, trans_letter_data_dict, trans_letter_columns

if __name__ == '__main__':
    app.run_server()