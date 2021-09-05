# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from scipy import signal
import numpy as np
from sklearn.metrics import mean_squared_error


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

t = np.linspace(0, 8*np.pi, 1000)
s = signal.sawtooth(t + np.pi, width = 1)

app.layout = html.Div(children=[
    html.H1(children='Test your Fourier approximation skills!'),

    dcc.Slider(
        id='a_1',
        min=-2.5,
        max=2.5,
        step=0.01,
        value=2,
    ),
    dcc.Slider(
        id='a_2',
        min=-2.5,
        max=2.5,
        step=0.01,
        value=0,
    ),
    dcc.Slider(
        id='a_3',
        min=-2.5,
        max=2.5,
        step=0.01,
        value=0,
    ),
    dcc.Slider(
        id='a_4',
        min=-2.5,
        max=2.5,
        step=0.01,
        value=0,
    ),
    dcc.Slider(
        id='a_5',
        min=-2.5,
        max=2.5,
        step=0.01,
        value=0,
    ),

    html.Div(id='slider-output-container'),

    dcc.Graph(
        id='approximation'
    ),

    dcc.Graph(
        id='error',
    )
])

@app.callback(
    dash.dependencies.Output('approximation', 'figure'),
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Output('error', 'figure'),
    [
        dash.dependencies.Input('a_1', 'value'),
        dash.dependencies.Input('a_2', 'value'),
        dash.dependencies.Input('a_3', 'value'),
        dash.dependencies.Input('a_4', 'value'),
        dash.dependencies.Input('a_5', 'value')
    ]
)
def update_figure(a_1, a_2, a_3, a_4, a_5):

    df = pd.DataFrame({
        "x": t,
        "y": np.pi * s ,
        "signal": ["sawtooth" for t in t]
    })


    df = df.append(
        pd.DataFrame({
            "x": t,
            "y": a_1 * np.sin(t) + a_2 * np.sin(2*t) + a_3 * np.sin(3*t) + a_4 * np.sin(4*t) + a_5 * np.sin(5*t),
            "signal": ["fourier" for t in t]
        })
    )

    fig_lines = px.line(df, x='x', y='y', color='signal', title='Sawtooth' )

    error_df = df[(df.x >= np.pi) & (df.x < 3*np.pi)]
    error = mean_squared_error(
        error_df[error_df.signal=='sawtooth'].y,
        error_df[error_df.signal=='fourier'].y)

    fig_error = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = error,
            title = {'text': "Mean squared error"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 10]},
                    'threshold' : {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.37211
                        }
                    }))

    function_string = 'f(t) = 0 + {a_1} * sin(t) + {a_2} * sin(2t) + {a_3} * sin(3t) + {a_4} * sin(4t) + {a_5} * sin(5t)'.format(a_1=a_1, a_2=a_2, a_3=a_3, a_4=a_4, a_5=a_5) 


    return fig_lines, 'You have selected ' + function_string, fig_error

if __name__ == '__main__':
    app.run_server(debug=True)