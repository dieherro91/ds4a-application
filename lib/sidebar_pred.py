# Basics Requirements
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from pages import homes
from datetime import date


# Recall app
from app import app

DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("c1logo_color.webp"), id="ds4a-image_pre",)],className='text-center')
 
############################################################################# 
# Titles
#############################################################################

titleAnalysisType=html.Div(children=[html.H6('ANALYSIS TYPE SELECTION', id='titleAnalysisType_id_pre', className='item-selection',),],)
titleZone=html.Div(children=[html.H6('ZONE SELECTION', id='titleZone_id_pre', className='item-selection',),],)
titleRoute=html.Div(children=[html.H6('ROUTE SELECTION', id='titleRoute_id_pre', className='item-selection',),],)

title_date_range=html.Div(children=[html.H6('TRAINING DATE', id='title_month_pre', className='item-selection',),],)
title_date_range_pre=html.Div(children=[html.H6('PREDICTION DATE', id='title_month_pre_date', className='item-selection',),],)
title_date_exclutor=html.Div(children=[html.H6('DATE EXCLUDER', id='title_exlutor_pre', className='item-selection',),],)
#############################################################################
# Dropdown Card
#############################################################################

drop_Type=html.Div(children=[dcc.Dropdown(id='type_dropdown_pre',options=[
        {'label': 'Route Analysis', 'value': 'Route Analysis'},
        {'label': 'Zone Analysis', 'value': 'Zone Analysis'}],value='',
                                          style={'font-size':'12'},
                                          placeholder="Select analysis type",),],)

drop_zone=html.Div(children=[dcc.Dropdown(id='zone_dropdown_pre',options=homes.list_zones,value='',
                                          style={'font-size':'12'},
                                          placeholder="Select a zone",),],)

drop_route=html.Div(children=[dcc.Dropdown(id='route_dropdown_pre',options=[],
                                           value='',style={'font-size':'12'},
                                           placeholder="Select a route",searchable=True,),],)

date_selector=html.Div(children=[
    title_date_range,
    dcc.DatePickerRange(
        id='my-date-picker-range_pre',
        calendar_orientation='horizontal',
        min_date_allowed=homes.date_min,
        max_date_allowed=homes.date_max,
        start_date=homes.date_min,
        initial_visible_month=date(2021, 4, 15),
        clearable =True,
        end_date=homes.date_max,
        #start_date=date(2021, 4, 15),
        month_format='YYYY-MM-DD',
    ),],)

date_excluder=html.Div(children=[
    title_date_exclutor,
    dcc.DatePickerSingle(
        id='date_picker_excluder_pre',
        calendar_orientation='horizontal',
        min_date_allowed=homes.date_min,
        max_date_allowed=homes.date_max,
        initial_visible_month=date(2021, 4, 15),        
        month_format='YYYY-MM-DD',
        clearable=True,),
    html.Hr(),
    html.Button('clear list', id='btn_pre', n_clicks=0,),
    dbc.Card(id='card_text_pre',children=[html.H6(" ",id="contador_pre",style = {"float":"left",'width': '85px'},),]),
    ],)

date_prediction=html.Div(children=[
    title_date_range_pre,
    dcc.DatePickerSingle(
        id='date_picker_predictor_pre',
        calendar_orientation='horizontal',
        initial_visible_month=date(2021, 7, 5),        
        month_format='YYYY-MM-DD',
        clearable=True,),
    html.Hr(),
    ],)

bottoms_update=html.Div(children=[html.Button('Prediction Data', id='btn_update_pre', n_clicks=0,
                                              style={'margin-left':'50px','margin-right': '50px'}),
                                  ])

#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [ 
        DS4A_Img,
        html.Hr(), 
        html.Div([titleZone, drop_zone,]),        
        html.Hr(),
        html.Div([titleRoute, drop_route,]),
        html.Hr(),
        date_excluder,
        html.Hr(),
        date_prediction,
        html.Hr(),
        date_selector,
        html.Hr(),
        html.Div([bottoms_update]),
        html.Hr(),
    ],
    className="ds4a-sidebar",
)
#.ds4a-sidebar