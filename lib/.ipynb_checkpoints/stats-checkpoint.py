import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import os

# Recall app
from app import app
from data import models
from views import figure

"""
DATA_DIR = "data"
superstore_path = os.path.join(DATA_DIR, "superstore.csv")

df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])
"""


##############################################################
# SCATTER PLOT
###############################################################

scatter_num=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='scatter_graph_route',),],),])
map_validaciones_ubication_zone_route=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='map_graph_route',),],),])




###############################################################
# LINE PLOT
###############################################################


#################################################################################,width={"size": 1, "order": 1, "offset": 3}
# Here the layout for the plots to use. width={"size": 3, "order": 2, "offset": 3}
##################################################################################style={width=100%,}

stats = dbc.Container(
    [
        
        # Place the different graph components here.
        
        
        dbc.Row([
            dbc.Col([scatter_num], width=6),
            dbc.Col(),
                ],align="center",no_gutters=True),
        
        dbc.Row([ dbc.Col(html.H6()),],align="center",no_gutters=True),        
        
    ],
    className="ds4a-body",
)
#DS4A_Img2 = html.Div(children=[html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"), id="ds4a-image2",style={'height':'10%', 'width':'10%'})],)