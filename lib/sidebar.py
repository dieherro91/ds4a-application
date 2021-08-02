# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt

# Recall app
from app import app
from data import models

####################################################################################
# Add the DS4A_Img
####################################################################################

# DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("c1_logo_tagline.svg"), id="ds4a-image",)],)
DS4A_Img = html.Div(children=[html.Img(src="https://www.correlation-one.com/hubfs/c1logo_color.png", id="ds4a-image",)],)

#DS4A_Img2 = html.Div(children=[html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"), id="ds4a-image2",)],)
############################################################################# 
# Titles
#############################################################################

titleAnalysisType=html.Div(children=[html.H6('ANALYSIS TYPE SELECTION', id='titleAnalysisType_id', className='item-selection',),],)
titleZone=html.Div(children=[html.H6('ZONE SELECTION', id='titleZone_id', className='item-selection',),],)
titleRoute=html.Div(children=[html.H6('ROUTE SELECTION', id='titleRoute_id', className='item-selection hidden',),],)

#############################################################################
# State Dropdown Card
#############################################################################



drop_Type=html.Div(children=[dcc.Dropdown(id='type_dropdown',options=[
        {'label': 'Route Analysis', 'value': 'Route Analysis'},
        {'label': 'Zone Analysis', 'value': 'Zone Analysis'}],value='', placeholder="Select analysis type",),],)

drop_zone=html.Div(children=[dcc.Dropdown(id='zone_dropdown',options=models.listZone(),value='',
                                          placeholder="Select a zone",),],)

drop_route=html.Div(children=[dcc.Dropdown(id='route_dropdown',options=[],
                                           value='',style={'display': 'none'},placeholder="Select a route",searchable=True,),],)



##############################################################################
# Date Picker Card
##############################################################################


#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [ 
        DS4A_Img,  # Add the DS4A_Img located in the assets folder
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        #html.h1
        html.Div([titleAnalysisType, drop_Type,]),
        html.Hr(), 
        html.Div([titleZone, drop_zone,]),        
        html.Hr(),
        html.Div([titleRoute, drop_route,]),
        html.Hr(),
        #DS4A_Img2,
        #html.Hr(),
    ],
    className="ds4a-sidebar",
)
#.ds4a-sidebar