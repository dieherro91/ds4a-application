# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Recall app
from app import app

title_principal = html.Div(children=[html.H1("Masivo Capital Data Analysis")], id="title_principal")
title_sub = html.Div(children=[html.H3("Select type of Data Analysis")], id="subtitle")
title = html.Div(className="ds4a-title",children=
    [
    title_principal,
    html.Hr(), 
    title_sub,
    html.Hr(), 
])

