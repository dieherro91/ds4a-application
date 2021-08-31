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
from datetime import date

# Recall app
from app import app

from pages import homes



DS4A_Img = html.Div(children=[html.Img(src="https://www.correlation-one.com/hubfs/c1logo_color.png", id="ds4a-image",)],className='text-center')

titleAnalysisType=html.Div(children=[html.H6('ANALYSIS TYPE SELECTION', id='titleAnalysisType_id', className='item-selection',),],)
titleZone=html.Div(children=[html.H6('ZONE SELECTION', id='titleZone_id', className='item-selection',),],)
titleRoute=html.Div(children=[html.H6('ROUTE SELECTION', id='titleRoute_id', className='item-selection hidden',),],)

title_date_range=html.Div(children=[html.H6('DATE SELECTOR', id='title_month', className='item-selection',),],)
title_date_exclutor=html.Div(children=[html.H6('DATE EXCLUDER', id='title_exlutor', className='item-selection',),],)


#############################################################################
# Dropdown 
#############################################################################


drop_Type=html.Div(children=[dcc.Dropdown(id='type_dropdown',options=[
        {'label': 'Route Analysis', 'value': 'Route Analysis'},
        {'label': 'Zone Analysis', 'value': 'Zone Analysis'}],value='',
                                          style={'font-size':'12'},
                                          placeholder="Select analysis type",),],)

drop_zone=html.Div(children=[dcc.Dropdown(id='zone_dropdown',options=homes.list_zones,value='',
                                          style={'font-size':'12'},
                                          placeholder="Select a zone",),],)

drop_route=html.Div(children=[dcc.Dropdown(id='route_dropdown',options=[],
                                           value='',style={'font-size':'12','display':'None'},
                                           placeholder="Select a route",searchable=True,),],)

date_selector=html.Div(children=[
    title_date_range,
    dcc.DatePickerRange(
        id='my-date-picker-range',
        calendar_orientation='horizontal',
        min_date_allowed=homes.date_min,
        max_date_allowed=homes.date_max,
        initial_visible_month=date(2021, 4, 15),
        clearable =True,
        #end_date=date(2021, 4, 15),
        #start_date=date(2021, 4, 15),
        month_format='YYYY-MM-DD',
        
    ),],)
date_excluder=html.Div(children=[
    
    title_date_exclutor,
    dcc.DatePickerSingle(
        id='date_picker_excluder',
        calendar_orientation='horizontal',
        min_date_allowed=homes.date_min,
        max_date_allowed=homes.date_max,
        initial_visible_month=date(2021, 4, 15),        
        month_format='YYYY-MM-DD',
        clearable=True,),
        
    html.Hr(),
    html.Button('clear list', id='btn', n_clicks=0,),
    dbc.Card(id='card_text',children=[html.H6(" ",id="contador",style = {"float":"left",'width': '85px'},),]),
    ],)


bottoms_update=html.Div(children=[html.Button('analysis Data', id='btn_update', n_clicks=0,
                                              style={'margin-left':'60px','margin-right': '60px'}),
                                  ]
                       )
##############################################################################
# Date Picker Card
##############################################################################


#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [ 
        # DS4A_Img, 
        ####################################################
        # Place the rest of Layout here
        #html.h1
        
        html.Hr(),
        html.Div([titleAnalysisType, drop_Type,]),
        html.Hr(), 
        html.Div([titleZone, drop_zone,]),        
        html.Hr(),
        html.Div([titleRoute, drop_route,]),
        html.Hr(),
        date_selector,
        html.Hr(),
        date_excluder,
        html.Hr(),
        html.Div([bottoms_update]),
        html.Hr(),
        
    ],
    className="ds4a-sidebar",
)
#.ds4a-sidebar