import psycopg2, psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import folium
from folium.plugins import HeatMap
import plotly.express as px
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# LOAD HELP PACKAGES
from lib import functions, analyticsData as AD



# Create the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = dash.Dash(__name__,
                requests_pathname_prefix=request_path_prefix,
                external_stylesheets=external_stylesheets)


# https://workspace.ds4a.com/user/joseavilesmnt@gmail.com/proxy/8050/


graphic1 =  dcc.Graph(
            id='example-graph',
            figure=AD.average_1()
        )

graphic2 =  dcc.Graph(
        id='example-graph2',
        figure=AD.demand_1()
    )

graphic3 =  dcc.Graph(
        id='example-graph3',
        figure=AD.heatmap_pasajeros()
    )



header =  html.H1(children='Dashboard Analytics',
            className="header")

DS4A_logo = html.Div(
    children=[html.Img(src=app.get_asset_url("c1_logo.svg"), id="ds4a-logo", className="logo" )],
)

# logo = html.H2('')

all_options = {
    'Ruta 1': ['zona azq', 'zona azt', 'zona aprr'],
    'Ruta 2': ['zona bzq', 'zona bdq', 'zona bteq'],
    'Ruta 3': ['zona czq', 'zona ctu', 'zona chtq'],
    'Ruta 4': ['zona dzq', 'zona szf', 'zona yzq']
}


# sidebar =  html.Div([
#     DS4A_logo,
#     html.Label('Routes',className="label" ),
#     dcc.Dropdown(
#         options=[
#             {'label': 'Route 1', 'value': 'RT1'},
#             {'label': 'Route 2', 'value': 'RT2'},
#             {'label': 'Route 3', 'value': 'RT3'}
#         ],
#         value='RT2'
#     )
# ], className="sidebar")


sidebar = html.Div([
    DS4A_logo,
    html.Hr(),
    dcc.RadioItems(
        id='rutas-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Ruta 1'
    ),

    html.Hr(),

    dcc.RadioItems(id='zonas-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
], className="sidebar")

@app.callback(
    Output('zonas-radio', 'options'),
    Input('rutas-radio', 'value'))
def set_cities_options(selected_ruta):
    return [{'label': i, 'value': i} for i in all_options[selected_ruta]]


@app.callback(
    Output('zonas-radio', 'value'),
    Input('zonas-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


# @app.callback(
#     Output('display-selected-values', 'children'),
#     Input('rutas-radio', 'value'),
#     Input('zonas-radio', 'value'))
# def set_display_children(selected_ruta, selected_zona):
#     return u'{} is a city in {}'.format(
#         selected_zona, selected_ruta,
#     )


heat_map_paradero = html.Div([
     
    html.Label('Routes',className="label" ),
    dcc.Dropdown(
        options=[
            {'label': 'Zona 1', 'value': 'z1'},
            {'label': 'Zona 2', 'value': 'z2'},
            {'label': 'Zona 3', 'value': 'z3'}
        ],
        value='z2'
    ),
    graphic3
])

main = html.Div([
#      functions.generate_table(df_promedios),
     heat_map_paradero,
     graphic1,
     graphic2
], className="main")
    



app.layout = html.Div(children=[
        header,
        sidebar,
       
        main
])

# Start the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)
