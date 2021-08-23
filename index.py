# Basics Requirements
import pathlib
import os
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app


###########################################################
#
#           APP LAYOUT:
#
###########################################################

# LOAD THE DIFFERENT FILES
from lib import title, sidebar, stats
from data import models
from views import figure
# PLACE THE COMPONENTS IN THE LAYOUT
# content = html.Div(id="page-content", className='content')

DS4A_logo = html.Div(
    children=[html.Img(src=app.get_asset_url("c1_logo.svg"), id="ds4a-logo", className="logo" )],
)

# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login',refresh=False),
            DS4A_logo,
            html.Label('UserName',className="label"),
            dcc.Input(id='user',value='', type='text'),
            html.Label('Password',className="label"),
            dcc.Input(id='passw',value='', type='password'),
            html.Button('Login',className="login-button", id='btnLogin', n_clicks=0,),
        ], className="login")




app.layout = html.Div(
    # [
    # dcc.Location(id='url', refresh=False),
    # dcc.Location(id='redirect', refresh=True)
    # ],

 
    [  title.title, sidebar.sidebar, stats.stats, ],
    # className="ds4a-app",  # You can also add your own css files by storing them in the assets folder
    
    id='output1',
    )

@app.callback(
    dash.dependencies.Output('output1', 'children'),
   [dash.dependencies.Input('btnLogin', 'n_clicks')],
    state=[State('user', 'value'),
                State('passw', 'value')])
def update_output(n_clicks, uname, passw):
    li={'admin':'admin123'}
    if uname =='' or uname == None or passw =='' or passw == None:
        return html.Div(children='')
    if uname not in li:
        return html.Div(children='Incorrect Username')
    if li[uname]==passw:
        return html.Div(dcc.Link('Access Granted!', href='/next_page'))
    else:
        return html.Div(children='Incorrect Password')


###############################################
#
#           APP INTERACTIVITY:
#
###############################################

#############################################################################################################
#################################################################
# dropdown sidebar available in the app.
#################################################################
@app.callback(
    Output('zone_dropdown','disabled'),
    Output('route_dropdown','disabled'),
    Output('route_dropdown','style'),
    Output('route_dropdown','value'),
    Output('titleRoute_id','style'),
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),  
)
def drowdownSelection(types_drop_value, zones_drop_value):
    if types_drop_value == '':
        return True, True, {'display': 'none'},'',{'textAlign': 'center','display': 'none'}
    elif types_drop_value!='':
        if types_drop_value=='Zone Analysis':
            return False, True, {'display': 'none'},'',{'textAlign': 'center','display': 'none'}
        elif types_drop_value=='Route Analysis':
            return False, False, {'display': 'block'},'',{'textAlign': 'center','display': 'block'}
        
#################################################################
# title lable type analysis in the app.
#################################################################
@app.callback(
    Output('subtitle','children'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
)
def drowdownSelection(types_drop_value,zone_drop_value,route_drop_value):
    if types_drop_value == '':
        return html.H3('   ')
    elif route_drop_value!='':
        return html.H3('{}: {} route: {}'.format(types_drop_value,zone_drop_value,route_drop_value))
        
    return html.H3('{}: {}  {}'.format(types_drop_value,zone_drop_value,route_drop_value))

#################################################################
# # dropdown sidebar values route in the app.
#################################################################    
@app.callback(
    Output('route_dropdown','options'),
    Input('zone_dropdown','value'), 
)
def drowdownSelection_route(zone_drop_value):        
    return models.ruta_comercial(zone_drop_value)

#############################################################################################################


#############################################################################################################
#############################################################
# scatter PLOT : Add sidebar interaction here
#############################################################zonal
@app.callback(
    Output('scatter_graph_zone', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_cluster_zone(month_scatter,typeValue,ZoneValue,RouteValue):
    
    if typeValue=='Zone Analysis' and ZoneValue!='' and month_scatter!='':
        return figure.make_graph_zonal(month_scatter,ZoneValue)
    elif RouteValue=='' or month_scatter=='':
        return px.scatter()
    else:
        return figure.make_graph_zonal(month_scatter,ZoneValue)
################################################################route_single
@app.callback(
    Output('scatter_graph_single_route', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_cluster_route(month_scatter,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month_scatter!='':
        return figure.make_graph_route_single(month_scatter,ZoneValue,RouteValue)
    elif RouteValue=='' or month_scatter=='':
        return px.scatter()
    else:
        return figure.make_graph_route_single(month_scatter,ZoneValue,RouteValue)
 ################################################################   
    
"""    
FALTA EL CALLBACK DEL ROUTESINGLE_HOUR este el id id='scatter_graph_single_route_hour    
"""  
    
#############################################################
# MAP : single route
#############################################################
    

@app.callback(
    Output('map_graph_route', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_map(month,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month !='':
        return figure.graph1_validaciones_ubication_zone(month,ZoneValue)
    elif RouteValue=='' or month=='':
        fig=px.scatter(None)
        return fig
    else:
        return figure.graph1_validaciones_ubication_zone_route(month,ZoneValue,RouteValue)

#############################################################
# HISTOGRAM : Add interactions here
#############################################################
@app.callback(
    Output('histogram_validation', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_histogram(month,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':
        return figure.histogram_validations_zone(month,ZoneValue)
    elif RouteValue=='' or month=='':
        fig=px.histogram()
        return fig
    else:
        return figure.histogram_validations(month,ZoneValue,RouteValue)   

#############################################################
# HEATMAP : Add interactions here
#############################################################
@app.callback(
    Output('heatmap_validation', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_histogram(month,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':
        return figure.heat_map_interactivition_zone(month,ZoneValue) 
    elif RouteValue=='' or month=='':
        fig=px.density_heatmap()
        return fig
    else:
        return figure.heat_map_interactivition(month,ZoneValue,RouteValue)   
    
#############################################################
# BARPLOT  : Add BARPLOT interaction here
#############################################################
@app.callback(
    Output('average_number_buses_per_day', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    
)
def make_graph_bar_avera(month,typeValue,ZoneValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':
        return figure.average_number_buses_per_day_per_month_zone(month,ZoneValue) 
    else:
        return px.scatter()

@app.callback(
    Output('average_number_buses_per_hour' , 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
    
)
def make_graph_bar_avera(month,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':        
        return figure.average_number_buses_per_hour_zone(month,ZoneValue) 
    elif RouteValue=='' or month=='':
        fig=px.density_heatmap()
        return fig
    else:
        return figure.average_number_buses_per_hour_route(month,ZoneValue,RouteValue)  
   
  

#############################################################
# PROFITS BY CATEGORY : Add sidebar interaction here
#############################################################




#############################################################
# MAP : Add interactions here
#############################################################

# MAP date interaction


# MAP click interaction


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)