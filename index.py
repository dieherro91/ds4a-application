# Basics Requirements
import pathlib
import os
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash import no_update

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
from lib import title, sidebar, stats, login, homes, prediction, team_83
from data import models
from views import figure

from auth import authenticate_user, validate_login_session
from server import app, server


from flask import session, copy_current_request_context

# local imports



###################################################3
###################################################
# login layout content
def login_layout():
    return login.login_users
    
# home layout content with logout botton
@validate_login_session
def app_layout():
    return homes.main_home_page

#################################################################
#### this fragment is the main app \(._.)/ for callbacks home
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',)
], className='wrapper-container')

#################################################################
#########analysis page
def analysis_page():
    return stats.analysis_page

#########prediction page
def prediction_part():
    return prediction.prediction_page

#########about_us page
def about_us_team():
    return team_83.about_us_page

###############################################################################
# utilities to login
###############################################################################

# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
    if url=='/home':
        return app_layout()
    elif url=='/login':
        return login_layout()
    elif url=='/analysis_data':
        return analysis_page()
    elif url=='/predictic_model':
        return prediction_part()
    elif url=='/About_Us':
        return about_us_team()
    else:
        return login_layout()

# authenticate the users ############################
@app.callback(
    [Output('url','pathname'),
     Output('login-alert','children')],
    [Input('login-button','n_clicks')],
    [State('login-email','value'),
     State('login-password','value')])
def login_auth(n_clicks,email,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update
    credentials = {'user':email,"password":pw}
    if authenticate_user(credentials):
        session['authed'] = True
        return '/home',''
    session['authed'] = False
    return no_update,dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)

##########logout callback#######################################################
@app.callback(
    Output('home-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
@app.callback(
    Output('analysis-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
@app.callback(
    Output('prediciton-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
@app.callback(
    Output('team_83_about-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
###############################################################################
#end of utilities
###############################################################################


#blank graph
variable_empty={ "layout": {
    "xaxis": {
        "visible": False }, "yaxis": {"visible": False},
    "annotations": [{"text": "Don´t have validations in those days","xref": "paper",'bgcolor':"#073559","yref":"paper","showarrow": False,"font": {"size":28}}],'bgcolor':"#073559",'paper_bgcolor':"#073559",'plot_bgcolor':"#073559"}}
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
        return True, True, {'display': 'none'},'19-11',{'textAlign': 'center','display': 'none'}
    elif types_drop_value!='':
        if types_drop_value=='Zone Analysis':
            return False, True, {'display': 'none'},'19-11',{'textAlign': 'center','display': 'none'}
        elif types_drop_value=='Route Analysis':
            return False, False, {'display': 'block'},'19-11',{'textAlign': 'center','display': 'block'}
        
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

                                                        #Graficos callbacks

#############################################################################################################
#############################################################
# scatter PLOT : Add sidebar interaction here
#############################################################zonal
@app.callback(
    Output('scatter_graph_zone', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_cluster_zone(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    try:
        fig=figure.make_graph_zonal(start_date,end_date,ZoneValue,a)
    except:
        return variable_empty   
    
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':
        return fig
    elif RouteValue=='' or end_date=='':
        return fig
    else:
        return fig
################################################################route_single
@app.callback(
    Output('scatter_graph_single_route', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_cluster_route(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    try:
        models.verificacion_fechas(start_date,end_date,ZoneValue,route,a)#####################
    except:
        return variable_empty  
    
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':
        return figure.make_graph_route_single(start_date,end_date,ZoneValue,RouteValue,a)
    elif RouteValue=='' or end_date=='':
        return figure.make_graph_route_single(start_date,end_date,ZoneValue,'19-11',a)
    else:
        return figure.make_graph_route_single(start_date,end_date,ZoneValue,RouteValue,a)
 ################################################################   
    
"""    
FALTA EL CALLBACK DEL ROUTESINGLE_HOUR este el id id='scatter_graph_single_route_hour    
"""  
    
#############################################################
# MAP : single route
#############################################################
    

@app.callback(
    Output('map_graph_route', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_map(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date !='':
        return figure.graph1_validaciones_ubication_zone(start_date,end_date,ZoneValue,a)
    elif RouteValue=='' or end_date=='':
        return figure.graph1_validaciones_ubication_zone_route(start_date,end_date,ZoneValue,'19-11',a)
    else:
        try:
            fig=figure.graph1_validaciones_ubication_zone_route(start_date,end_date,ZoneValue,RouteValue,a)
        except:
            return variable_empty 
        return fig
        

#############################################################
# HISTOGRAM : Add interactions here
#############################################################
@app.callback(
    Output('histogram_validation', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_histogram(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
        
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':
        return figure.histogram_validations_zone(start_date,end_date,ZoneValue,a)
    elif RouteValue=='' or end_date=='':
        return figure.histogram_validations(start_date,end_date,ZoneValue,'19-11',a) 
    else:
        try:
            fig=figure.histogram_validations(start_date,end_date,ZoneValue,RouteValue,a)   
        except:
            return variable_empty 
        return fig  

#############################################################
# HEATMAP : Add interactions here
#############################################################
@app.callback(
    Output('heatmap_validation', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_heat_maps(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':
        return figure.heat_map_interactivition_zone(start_date,end_date,ZoneValue,a) 
    elif RouteValue=='' or end_date=='':
        return figure.heat_map_interactivition(start_date,end_date,ZoneValue,'19-11',a)   
    else:
        try:
            fig=figure.heat_map_interactivition(start_date,end_date,ZoneValue,RouteValue,a) 
        except:
            return variable_empty 
        return fig
    
#############################################################
# BARPLOT  : Add BARPLOT interaction here
#############################################################
@app.callback(
    Output('average_number_buses_per_day_all_routes', 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
)
def make_graph_bar_averas(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    try:
        fig=figure.average_number_buses_per_day_per_month_zone_all_routes(start_date,end_date,ZoneValue,a) 
    except:
        return variable_empty
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':
        return fig
    elif RouteValue=='' or end_date=='':
        return variable_empty
    else:
        return fig

@app.callback(
    Output('average_number_buses_per_hour' , 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
    
)
def make_graph_bar_avera(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':        
        return figure.average_number_buses_per_hour_zone(start_date,end_date,ZoneValue,a) 
    elif RouteValue=='' or end_date=='':
        return figure.average_number_buses_per_hour_route(start_date,end_date,ZoneValue,'19-11',a)  
    else:
        try:
            fig=figure.average_number_buses_per_hour_route(start_date,end_date,ZoneValue,RouteValue,a) 
        except:
            return variable_empty 
        return fig 

#################
#####################

@app.callback(
    Output('bar_total_valitations' , 'figure'),
    
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('type_dropdown','value'),
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'),
    
)
def make_graph_bar_total_hour(start_date,end_date,typeValue,ZoneValue,RouteValue):
    a=models.exclude(listas)
    if typeValue=='Zone Analysis' and ZoneValue!='' and end_date!='':        
        return figure.bar_total_valitations_zone_hour(start_date,end_date,ZoneValue,a)
    elif RouteValue=='' or end_date=='':
        return figure.bar_total_valitations_route_hour(start_date,end_date,ZoneValue,'19-11',a)
    else:
        try:
            fig=figure.bar_total_valitations_route_hour(start_date,end_date,ZoneValue,RouteValue,a)
        except:
            return variable_empty 
        return fig

############################################################excluder data##################
    
listas=[]
@app.callback(
    Output('contador', 'children'),
    Output('btn', 'n_clicks'),
    Output('type_dropdown','value'),
    
    Input('date_picker_excluder', 'date'),
    Input('btn', 'n_clicks'),
    Input('type_dropdown','value'),
)
def excluder_date_function(date_value,btn,type_value):
    
    if date_value is not None:
        listas.append(date_value)
    
    if btn != 0:
        
        listas.clear()
        return listas, 0, ''
        
    return listas, 0, type_value

#############################################################
# TABS CATEGORY : interaction here
#############################################################


################################################################
# MAP : Add interactions here
#############################################################

# MAP date interaction


# MAP click interaction


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)