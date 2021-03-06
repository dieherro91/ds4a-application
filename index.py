
### this  file is the main page were the code is executed
#  in this file are all the callbacks in the page

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash import no_update
from flask import session
import datetime
import time
import dash_bootstrap_components as dbc
from app import app

from pages import  login, homes, team_83
from data import models_analysis, list_training_data
from views import figure_analitic, figure_prediction
from content_apps import  analitics, prediction
from auth import authenticate_user, validate_login_session
from server import app

###################################################
###################################################

# login layout content
def login_layout():
    return login.login_users
    
# home layout content with logout botton
@validate_login_session
def app_layout():
    return homes.main_home_page

#################################################################
#### the fragment below is the "main app" \(._.)/ for callbacks home an links
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',)
], className='wrapper-container')

#################################################################
#########function that calls the analysis page
def analysis_page():
    return analitics.analysis_page

#########function that calls the prediction page
def prediction_part():
    return prediction.prediction_page

#########function that calls the about_us page
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
# Analysis plot Callsbacks for the analitic page  : 
#############################################################
@app.callback(
    Output('route_dropdown','value'),
    Output('route_dropdown','disabled'),
    Output('route_dropdown','style'),

    Input('type_dropdown','value'),   
)
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

#Callback to show the routes available for the zone selected 
@app.callback(
    Output('route_dropdown','options'),
    Input('zone_dropdown','value'), 
)
def drowdownSelection_route(zone_drop_value):
    lit=[{'label':'loading...','value':'loading...'}]
    
    if (zone_drop_value is None or zone_drop_value==''):
        return lit
    
    return homes.wer[zone_drop_value]

#############################################################################################################

            #Graficos callbacks for analitc page

#############################################################################################################


#blank graph used for the exception when filters dont have data or problems ocurrurs with the plot
text_for_blanck_graph="Missing filters for the data, (click again)"
variable_empty={ "layout": {
    "xaxis": {
        "visible": False }, "yaxis": {"visible": False},
    "annotations": [{"text": text_for_blanck_graph,"xref": "paper",'bgcolor':"#ffffff","yref":"paper","showarrow": False,"font": {"size":28}}],'bgcolor':"#073559",'paper_bgcolor':"#ffffff",'plot_bgcolor':"#ffffff"}}

############################################################excluder data##################


#callback for saving the dates to exclude for the queries.
listas=[]   # list where i saved the exclude dates don't deleted
@app.callback(
    Output('contador', 'children'),
    Output('btn', 'n_clicks'),
    
    Input('date_picker_excluder', 'date'),
    Input('btn', 'n_clicks'),
)
def excluder_date_function(date_value,btn):
    if date_value is not None:
        listas.append(date_value)
    if btn != 0:
        listas.clear()
        return listas, 0,
    return listas, 0

###################################################  Callbacks plots ###########################################

#### callback for the street map validations figure
@app.callback(
    Output('map_graph_route','figure'),
        
    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('route_dropdown','value'), 
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot1(n_clicks,types,zones,route,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        
        if (types=='Zone Analysis'):
            time.sleep(1)
            try:
                fig=figure_analitic.graph1_validaciones_ubication_zone_route(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty                
            return fig
        if (types=='Route Analysis' and route !=''):
            time.sleep(1)
            try:
                fig=figure_analitic.graph1_validaciones_ubication_zone_route(start_date,end_date,zones,route,a)
            except:
                fig=variable_empty
            return fig
    time.sleep(1)
    return variable_empty

#### callback for the scatter Average validations per bus vs number of buses used per zone figure
@app.callback(
    Output('scatter_graph_zone','figure'),
        
    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot2(n_clicks,types,zones,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (zones is not None):
            time.sleep(1)
            try:
                fig=figure_analitic.make_graph_zonal(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty
            return fig
    time.sleep(1)
    return variable_empty

#callback for the bar plot Average number of buses per day used per zone figure
@app.callback(
    Output('average_number_buses_per_day_all_routes','figure'),

    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot3(n_clicks,types,zones,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (zones is not None):
            time.sleep(1)
            try:
                fig=figure_analitic.average_number_buses_per_day_per_month_zone_all_routes(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty
            return fig
    time.sleep(1)
    return variable_empty

# callback return 2 figures for Total validations for each bus stop and hour figures.
@app.callback(
    Output('heatmap_validation','figure'),
    Output('bar_total_valitations','figure'),
    
    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('route_dropdown','value'), 
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot4_5(n_clicks,types,zones,route,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            time.sleep(1)
            try:
                fig, fig_1=figure_analitic.heat_map_interactivition(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty
                fig_1=variable_empty
            return fig , fig_1
        if (types=='Route Analysis' and route !=''):
            time.sleep(1)
            try:
                fig, fig_1=figure_analitic.heat_map_interactivition(start_date,end_date,zones,route,a)
            except:
                fig=variable_empty
                fig_1=variable_empty
            return fig, fig_1
    time.sleep(1)
    return variable_empty, variable_empty

#callback for the bar plot average bus per hour figure
@app.callback(
    Output('average_number_buses_per_hour','figure'),

    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('route_dropdown','value'), 
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot6(n_clicks,types,zones,route,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis

    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            time.sleep(1)
            try:
                fig=figure_analitic.average_number_buses_per_hour_route(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty
            return fig
        if (types=='Route Analysis' and route !=''):
            time.sleep(1)
            try:
                fig=figure_analitic.average_number_buses_per_hour_route(start_date,end_date,zones,route,a)
            except:
                fig=variable_empty
            return fig
    time.sleep(1)
    return variable_empty

#callback for the histogram validations per travel route 
@app.callback(    
    Output('histogram_validation', 'figure'),
    
    Input('btn_update','n_clicks'),
    State('type_dropdown','value'),    
    State('zone_dropdown','value'),
    State('route_dropdown','value'), 
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date'),
)
def saved_plot7(n_clicks,types,zones,route,start_date,end_date):
    a=models_analysis.exclude(listas)  #exclude from the analysis the list values in the analysis
    
    if (types!= '' and zones != '' and start_date != '' and end_date != '' ):
        if (types=='Zone Analysis'):
            time.sleep(1)
            try:
                fig=figure_analitic.histogram_validations(start_date,end_date,zones,' ',a)
            except:
                fig=variable_empty
            return fig
        if (types=='Route Analysis' and route !=''):
            time.sleep(1)
            try:
                fig=figure_analitic.histogram_validations(start_date,end_date,zones,route,a)
            except:
                fig=variable_empty
            return fig
    time.sleep(1)
    return variable_empty

#############################################################
# button sidebar analysis page
#############################################################

#Callback that trigger the plots for the analitic page
@app.callback(
    Output('replace_analysis','children'),
    Output('btn_update','n_clicks'),
    Output('confirm', 'displayed'),
    Input('btn_update','n_clicks'),
)  
def page_change(n_clicks):
    if n_clicks is None or n_clicks==0:

        return analitics.imagen_test, 0, False
    
    return analitics.analitics_stats, 0, True

    


#############################################################
# Predictic Callsbacks  : 
#############################################################
#############################################################

#callback how shows the routes available for the zone value
@app.callback(
    Output('route_dropdown_pre','options'),
    Input('zone_dropdown_pre','value'), 
)
def drowdownSelection_route(zone_drop_value):
    lit=[{'label':'loading...','value':'loading...'}]
    if (zone_drop_value is None or zone_drop_value==''):
        return lit
    
    return list_training_data.list_routes_available_predictc(zone_drop_value)



#############################################################################################################

            #Graficos callbacks for analitc page

#############################################################################################################





###################################################  Callbacks plots       ##########################

#Callback that make the figure for the clusterin and the table it change for the numbre of clusters selected
@app.callback(
    Output('clustering', 'figure'),
    Output('table_cluster','data'),

    Input("cluster-count", "value"),
    State('zone_dropdown_pre', 'value'),
    State('route_dropdown_pre', 'value'),
)
def making_cluster(n_clusters,zones,route):
    time.sleep(1)
    try:
        fig, df=figure_prediction.cluster(zones,n_clusters,route)
        data=df.to_dict('records')
    except:
        fig=variable_empty
        data=[{'cluster': 'faltan filtros',}]
    return fig, data


@app.callback(
    Output('map_graph_prediction_route','figure'),

    Input('btn_update_pre','n_clicks'),
    Input("selection_graph", "value"),
    Input('strike_day','value'),
    State('zone_dropdown_pre', 'value'),
    State('route_dropdown_pre','value'),
    State('date_picker_predictor_pre','date'),
    
)
def drowdownSelection_route(n_clicks,graph,strike,zones,route,days):
    animations=figure_prediction.map_street_predicted(zones,route,days,strike)

    if (strike == 'normal'):
        strikes=0
        animations=figure_prediction.map_street_predicted(zones,route,days,strikes)
        return animations[graph]
    if (strike == 'strike'):
        strikes=1
        animations=figure_prediction.map_street_predicted(zones,route,days,strikes)
        return animations[graph]
    else:
        return variable_empty



#############################################################
# button sidebar predictive page
#############################################################

#Callback that trigger the plots for the predictive page
@app.callback(
    Output('replace_analysis_prediction','children'),
    Output('btn_update_pre','n_clicks'),
    Input('btn_update_pre','n_clicks'),
)  
def page_change_pre(n_clicks):
    if n_clicks is None or n_clicks==0:
        return prediction.imagen_test, 0
    return prediction.prediction, 0
###########################################################################################################




if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)