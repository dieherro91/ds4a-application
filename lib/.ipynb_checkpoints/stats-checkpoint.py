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
"""
#################################################################
################################################################global dataframe ##############################################
df=pd.read_sql(" \
    WITH validaciones AS (\
        SELECT fecha_trx AS fecha_servicio,\
        date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 5) * interval '1 minute') AS hora_servicio,\
        paradero.id_paradero, \
        ruta_comercial,\
        cenefa, \
        vehiculo_id, \
        posicion,\
        latitud,\
        longitud, \
        descripcion_operador \
        FROM validacion\
        JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
        JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
        JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
        JOIN operador ON operador.id_operador = validacion.operador_id \
         \
        )\
          SELECT descripcion_operador AS operator, fecha_servicio AS date_validation, hora_servicio AS hour_validation, \
            ruta_comercial AS commertial_route, cenefa AS border, vehiculo_id AS vehicle_id,\
            ruta_comercial AS commertial_route , posicion AS position, latitud AS latitude, \
            longitud AS longitude, count(*) AS amount_validations FROM validaciones \
           \
          GROUP BY fecha_servicio, hora_servicio, ruta_comercial, cenefa, vehiculo_id, \
               posicion, latitud, longitud, descripcion_operador \
          ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;", connect_db.conn())
#############################################################################################################################

df['commertial_route']=df['commertial_route'].astype(str)
df['operator']=df['operator'].astype(str)
df['vehicle_id']=df['vehicle_id'].astype(str)
df['date_validation']=pd.to_datetime(df['date_validation'])
df['day_of_week']=df['date_validation'].dt.dayofweek


df1=df[(df["operator"]=='KENNEDY') & (df["date_validation"].dt.month==4)]
df4=df1
#df4.set_index('commertial_route', 'day_of_week', 'vehicle_id')
df4[['commertial_route','day_of_week','vehicle_id','amount_validations']].groupby(['commertial_route','day_of_week','vehicle_id']).agg({'amount_validations':'sum'})  
print("ahivimos")
#df1=df1.groupby(['day_of_week','vehicle_id','commertial_route'], as_index=False).aggregate({'sum_amount_validations':'sum'})
#df1=df1.groupby(['commertial_route','day_of_week'], as_index=False).aggregate({'vehicle_id':'count','amount_validations':'mean'})
dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
df1['day_of_week']=df1['day_of_week'].astype(str)
df1['day_of_week'].replace(dayWeek,inplace=True)

"""



##############################################################
# SCATTER PLOT
###############################################################

#scatter_global=make_graph_route(df1,4,'KENNEDY')
#



###############################################################
# LINE PLOT
###############################################################


##############################################################################################
#esta es una sola grafica usar como referencia la "scatter_num_zonal"

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
bar_average_number_buses_per_day_zone=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='average_number_buses_per_day',),],),])
bar_average_number_buses_per_hour=dbc.Card([dbc.FormGroup(children=[dcc.Graph(id='average_number_buses_per_hour',),],),])

############################################################################################################

tabs_controles=dcc.Tabs(id='tabs-example', value='tab-1', children=[
                            dcc.Tab(label='Month Analysis', value='tab-1'),
                            dcc.Tab(label='Week of the day and hour', value='tab-2'),
                            dcc.Tab(label='Predictions', value='tab-3'),
                                    ])
slider_hour=dcc.Slider(id='slider_hours', min=0, max=23, step=1, value=10,marks={
                                                            0: {'label': '0'},
                                                            7: {'label': '26'},
                                                            17: {'label': '37'},
                                                            23: {'label': '100'}
    })




#################################################################################,width={"size": 1, "order": 1, "offset": 3}
# Here the layout for the plots to use. width={"size": 3, "order": 2, "offset": 3}
##################################################################################style={width=100%,}

stats = html.Div(
    [
        # Place the different graph components here.
        dbc.Row([

            dbc.Col([map_validaciones_ubication_zone_route], width=6),
            dbc.Col(),

            dbc.Col([bar_average_number_buses_per_hour], width=6),
            dbc.Col([scatter_num_zonal], width=6),

                ],align="center",no_gutters=True),
        
        dbc.Row([ 
            dbc.Col(html.H6()),
            ],align="center",no_gutters=True),        
        
    ],
    className="ds4a-body",
)
#DS4A_Img2 = html.Div(children=[html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"), id="ds4a-image2",style={'height':'10%', 'width':'10%'})],)