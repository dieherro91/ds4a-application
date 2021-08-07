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


from data import connect_db

##############################################################
# SCATTER PLOT
###############################################################


scatter_num_zonal=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='scatter_graph_zone',),],),])

scatter_num_single_route=dbc.Card([dbc.FormGroup(children=[dcc.Graph(
                                                                id='scatter_graph_single_route',),],),])


scatter_num_single_route_hour=dbc.Card([dbc.FormGroup(children=[dcc.Graph(
                                                                id='scatter_graph_single_route_hour',),],),]) # pendiente por sliders#
#################################################################################################################################


map_validaciones_ubication_zone_route=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='map_graph_route',),],),])

histogram_validations_route=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='histogram_validation',),],),])


heat_map_route=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='heatmap_validation',),],),])

#######################################    only_zone_graphs      ###################################################
bar_average_number_buses_per_day_zone_all=dbc.Card([dbc.FormGroup(children=[
                                                    dcc.Graph(id='average_number_buses_per_day_all_routes',),],),])
bar_average_number_buses_per_hour=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='average_number_buses_per_hour',),],),])

############################################################################################################
#

slider_hour=dcc.Slider(id='slider_hours', min=0, max=23, step=1, value=10,marks={
                                                            0: {'label': '0'},
                                                            7: {'label': '26'},
                                                            17: {'label': '37'},
                                                            23: {'label': '100'}
    })


analysis_content=dbc.Container([ 
       ])

#################################################################################,width={"size": 1, "order": 1, "offset": 3}
# Here the layout for the plots to use. width={"size": 3, "order": 2, "offset": 3}
##################################################################################style={width=100%,}

stats = html.Div(
    [
        # Place the different graph components here.
        html.Div([map_validaciones_ubication_zone_route]),
       dbc.Row([
            
            dbc.Col([scatter_num_zonal,],align ='center', width="auto"),
            dbc.Col([bar_average_number_buses_per_day_zone_all ],width="auto"),            
                ],justify="start",className="Rowbody_1"),
        
       dbc.Row([
           dbc.Col([heat_map_route,],align ='center', width="auto"),
           dbc.Col([],align ='center', width="auto"),
               ],justify="start",className="Rowbody_2"), 
        
        dbc.Row([
            dbc.Col([bar_average_number_buses_per_hour],align ='center', width="auto"),
            dbc.Col([histogram_validations_route],align ='center', width="auto"),
           
               ],justify="start",className="Rowbody_3"), 
            
       
        
       dbc.Row([ 
            dbc.Col(html.H6("hallo",id="jed")),
            ],),
              
        
    ],
    className="ds4a-body",
)
#DS4A_Img2 = html.Div(children=[html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"), id="ds4a-image2",style={'height':'10%', 'width':'10%'})],)