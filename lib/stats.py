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
from lib import title, sidebar

from data import connect_db

##############################################################
# SCATTER PLOT
###############################################################


scatter_num_zonal=dbc.Card([dbc.CardBody([html.H4("Validations vs Number of Buses Per Day Week", className="card-title  text-muted font-graphics"),dcc.Graph(id='scatter_graph_zone',),],),])

scatter_num_single_route=dbc.Card([dbc.CardBody([html.H4("Card title", className="card-title"), 
dcc.Graph(
                                                                id='scatter_graph_single_route',),],),])


scatter_num_single_route_hour=dbc.Card([dbc.CardBody([html.H4("Card title", className="card-title"), 
dcc.Graph(
                                                                id='scatter_graph_single_route_hour',),],),]) # pendiente por sliders#
#################################################################################################################################


map_validaciones_ubication_zone_route=dbc.Card([dbc.CardBody([html.H4("Map Validations", className="card-title"), 
dcc.Graph(id='map_graph_route',),],),])

histogram_validations_route=dbc.Card([dbc.CardBody([html.H4("Histogram Validations Per Travel Route", className="card-title"), dcc.Graph(id='histogram_validation',),]),])


heat_map_route=dbc.Card([dbc.CardBody([html.H4("Validations Per Hour by Bus Stop", className="card-title"), 
dcc.Graph(id='heatmap_validation',),],),])

#######################################    only_zone_graphs      ###################################################
bar_average_number_buses_per_day_zone_all=dbc.Card([dbc.CardBody([html.H4("Average Quantity Buses per Zone", className="card-title"), 

                                                    dcc.Graph(id='average_number_buses_per_day_all_routes',),],),])
bar_average_number_buses_per_hour=dbc.Card([dbc.CardBody([html.H4("Average and Number Buses Per Hour", className="card-title"), 
dcc.Graph(id='average_number_buses_per_hour',),],),])

############################################################################################################

bar_total_validations_hour=dbc.Card([dbc.CardBody([html.H4("Total Validations Per Hour", className="card-title"), 
dcc.Graph(id='bar_total_valitations',),],),])


#################################################################################,width={"size": 1, "order": 1, "offset": 3}
# Here the layout for the plots to use. width={"size": 3, "order": 2, "offset": 3}
##################################################################################style={width=100%,}

stats = html.Div(
    [
        # Place the different graph components here.
       
        dbc.Row([
            dbc.Col([map_validaciones_ubication_zone_route], width="12", className='mt-1 mb-2 pl-1.5 pr-1.5')
        ], ),
        
       html.Br(), 
        
       dbc.Row([
            
            dbc.Col([scatter_num_zonal,],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
            dbc.Col([bar_average_number_buses_per_day_zone_all,],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
                        
                ],),
        
        html.Br(),
        
       dbc.Row([
           dbc.Col([heat_map_route,], width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
           dbc.Col([bar_total_validations_hour], width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
       
               ] ), 
        
        dbc.Row([
            dbc.Col([bar_average_number_buses_per_hour],width="6"),
            dbc.Col([histogram_validations_route],width="6"),
           
               ] ), 

              
        
    ],
    className="ds4a-body",
)

DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("pexels-nataliya-vaitkevich-7172856.jpg"), style={"width" : "700px" })],)
imagen_test= dbc.Jumbotron(id='jumboContainer',children=[
        dbc.Container(
            [
                html.Div([
                html.H1("Data Analysis", className="display-5"),
                html.P(
                    "espacio para escribir algo,"
                    "mas espacio para escribir algo.",
                    className="lead",
                ),
                DS4A_Img,
                ] ,className="text-center"),
                html.P(
                    "espacio para escirbir algunas cosas   "
                    "espacio para escirbir algunas cosas ."
                    "espacio para escirbir algunas cosas",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)


alert_no_dropdows=html.Div([html.Br(),
    dbc.Row([
                    html.Br(),
                    html.Br(),
                    dbc.Col([html.H1("Please complete the information in the sidebar")],
                width={"size": 12, "offset":1}, className='mt-1 mb-2 pl-1.5 pr-1.5'),
                     html.Br(),
                     ],className="ds4a-body",),]) 



analysis_page=html.Div(id='analysis_page_test',children=[dcc.Location(id='analysis-url',pathname='/analysis_data'),
                        title.navbar,
                        sidebar.sidebar,
                        html.Div(id='replace_analysis',children=[imagen_test]),
                ],className="container-fluid bg-app",
)





