import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import numpy as np
import plotly.express as px

# Page Layout
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Br(),
                     html.H1("Coming soon",
                            style={'textAlign': 'center'})],
                    className='mt-4')
        ])
    ])
])
