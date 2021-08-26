# Basics Requirements
import pathlib
import os
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
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

app.config.suppress_callback_exceptions = True

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
    Input('logout-button','n_clicks'),
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



#########################################################################
###############################################
#
#           APP INTERACTIVITY: 
#
###############################################


#############################################################
# Analysis plot Callsbacks  : 
#############################################################
@app.callback(
    Output('route_dropdown','value'),
    Output('route_dropdown','disabled'),
    Output('route_dropdown','style'),

    Input('type_dropdown','value'),   
)#
def drowdownSelection(types_drop_value):
    if types_drop_value == '':
        return '',True, {'display': 'none'}
    if types_drop_value == 'Zone Analysis':
        return '',True, {'display': 'none'}
    if types_drop_value == 'Route Analysis':
        return '',False, {'display': 'block'}
    
    return '',True, {'display': 'none'}
        
#################################################################


#################################################################
# # dropdown sidebar values route in the app.
#################################################################    
@app.callback(
    Output('route_dropdown','options'),
    Input('zone_dropdown','value'), 
)
def drowdownSelection_route(zone_drop_value):
    lit=[{'label':'loading...','value':'loading...'}]
    if (zone_drop_value is None or zone_drop_value==''):
        return lit
    return models.ruta_comercial(zone_drop_value)

#############################################################################################################

                                                        #Graficos callbacks

#############################################################################################################
#############################################################
# scatter PLOT : Add sidebar interaction here
#############################################################

#############################################################
# button sidebar CATEGORY : interaction here
#############################################################
#blank graph
variable_empty={ "layout": {
    "xaxis": {
        "visible": False }, "yaxis": {"visible": False},
    "annotations": [{"text": "Select filters for the data","xref": "paper",'bgcolor':"#ffffff","yref":"paper","showarrow": False,"font": {"size":28}}],'bgcolor':"#073559",'paper_bgcolor':"#ffffff",'plot_bgcolor':"#ffffff"}}

############################################################excluder data##################
    
listas=[]   # list where i saved the exclude dates don't deleted

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

###################################################  Callback ##################

@app.callback(
    Output('map_graph_route','figure'),
        
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot1(types,zones,route,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        
        if (types=='Zone Analysis'):
            return figure.graph1_validaciones_ubication_zone_route(start_date,end_date,zones,' ',a)
        if (types=='Route Analysis' and route !=''):
            return figure.graph1_validaciones_ubication_zone_route(start_date,end_date,zones,route,a)
        
    return variable_empty

@app.callback(
    Output('scatter_graph_zone','figure'),
        
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot2(types,zones,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (zones is not None):
            return figure.make_graph_zonal(start_date,end_date,zones,' ',a)
    return variable_empty

@app.callback(
    Output('average_number_buses_per_day_all_routes','figure'),

    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot3(types,zones,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (zones is not None):
            return figure.average_number_buses_per_day_per_month_zone_all_routes(start_date,end_date,zones,' ',a) 
    return variable_empty

@app.callback(
    Output('heatmap_validation','figure'),
    
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot4(types,zones,route,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            route=' '
            return figure.heat_map_interactivition(start_date,end_date,zones,route,a)
        if (types=='Route Analysis' and route !=''):
            return figure.heat_map_interactivition(start_date,end_date,zones,route,a)
    return variable_empty

@app.callback(
    Output('bar_total_valitations','figure'),
        
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot5(types,zones,route,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            return figure.bar_total_valitations_route_hour(start_date,end_date,zones,route,a)
        if (types=='Route Analysis' and route !=''):
            return figure.bar_total_valitations_route_hour(start_date,end_date,zones,route,a)   
    return variable_empty

@app.callback(
    Output('average_number_buses_per_hour','figure'),

    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot6(types,zones,route,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            return figure.average_number_buses_per_hour_route(start_date,end_date,zones,route,a)
        if (types=='Route Analysis' and route !=''):
            return figure.average_number_buses_per_hour_route(start_date,end_date,zones,route,a)
    return variable_empty


@app.callback(    
    Output('histogram_validation', 'figure'),
    
    Input('type_dropdown','value'),    
    Input('zone_dropdown','value'),
    Input('route_dropdown','value'), 
    Input('my-date-picker-range','start_date'),
    Input('my-date-picker-range','end_date'),
)
def saved_plot7(types,zones,route,start_date,end_date):
    a=models.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            return figure.histogram_validations(start_date,end_date,zones,route,a)
        if (types=='Route Analysis' and route !=''):
            return figure.histogram_validations(start_date,end_date,zones,route,a)
    return variable_empty

   
@app.callback(
    Output('replace_analysis','children'),
    Output('btn_update','n_clicks'),
    Input('btn_update','n_clicks'),
)  
def page_change(n_clicks):
    if n_clicks is None or n_clicks==0:
        return stats.imagen_test, 0
    return stats.stats, 0

    

##########################################################################################################################
# Predictic Callsbacks  : 
##########################################################################################################################


@app.callback(
    Output('replace_analysis_prediction','children'),
    Output('btn_update_pre','n_clicks'),
    Input('btn_update_pre','n_clicks'),
)  
def page_change_pre(n_clicks):
    if n_clicks is None or n_clicks==0:
        return prediction.imagen_test, 0
    return prediction.prediction, 0













# MAP date interaction


# MAP click interaction


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)