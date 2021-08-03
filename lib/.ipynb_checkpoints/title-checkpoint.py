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
logo_masivo = html.Img(src=app.get_asset_url("logo-masivo.png"), id="ds4a-logo-masivo")

title_principal = html.Div(children=[
    html.H3("Masivo Capital Data Analysis"),
    # logo_masivo,
    ], id="title-principal")
title_sub = html.Div(children=[html.H3("Select type of Data Analysis")], id="subtitle")


title = html.Div(className="ds4a-title",children=
    [
    title_principal,

])
tisdf=dbc.Container([dbc.Row([   ]),align="center",no_gutters=True,])
