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

app.layout = html.Div(
    [  title.title, sidebar.sidebar, stats.stats, ],
    className="ds4a-app",  # You can also add your own css files by storing them in the assets folder
)

#########################################################################
variable_empty={ "layout": {
    "xaxis": {
        "visible": False }, "yaxis": {"visible": False},
    "annotations": [{"text": "","xref": "paper",'bgcolor':"#073559","yref":"paper","showarrow": False,"font": {"size":28}}],'bgcolor':"#073559",'paper_bgcolor':"#073559",'plot_bgcolor':"#073559"}}
#########################################################################
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
    #
    fig=figure.make_graph_zonal(month_scatter,ZoneValue)
    if typeValue=='Zone Analysis' and ZoneValue!='' and month_scatter!='':
        return fig
    elif RouteValue=='' or month_scatter=='':
        return variable_empty
    else:
        return fig
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
        return variable_empty
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
        return variable_empty
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
        return variable_empty
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
def make_graph_heat_maps(month,typeValue,ZoneValue,RouteValue):
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':
        return figure.heat_map_interactivition_zone(month,ZoneValue) 
    elif RouteValue=='' or month=='':
        return variable_empty
    else:
        return figure.heat_map_interactivition(month,ZoneValue,RouteValue)   
    
#############################################################
# BARPLOT  : Add BARPLOT interaction here
#############################################################
@app.callback(
    Output('average_number_buses_per_day_all_routes', 'figure'),
    Input("control_month_scatter", "value"),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_bar_averas(month,typeValue,ZoneValue,RouteValue):
    fig=figure.average_number_buses_per_day_per_month_zone_all_routes(month,ZoneValue) 
    if typeValue=='Zone Analysis' and ZoneValue!='' and month!='':
        return fig
    elif RouteValue=='' or month=='':
        return variable_empty
    else:
        return fig

"""
fig=figure.make_graph_zonal(month_scatter,ZoneValue)
    if typeValue=='Zone Analysis' and ZoneValue!='' and month_scatter!='':
        return fig
    elif RouteValue=='' or month_scatter=='':
        return px.scatter([],[],width=400, height=300)
    else:
        return fig
"""    
    

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
        return variable_empty
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