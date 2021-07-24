import psycopg2, psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import folium
from folium.plugins import HeatMap
import plotly.express as px
import os
import dash
import dash_core_components as dcc
import dash_html_components as html

# Create the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = dash.Dash(__name__,
                requests_pathname_prefix=request_path_prefix,
                external_stylesheets=external_stylesheets)

DB = 'masivo_sitp_2'
USER = 'postgres'
PORT =5432
PASSWORD = '4ng3lDS4A*83'
HOST='ds4a-83rds.ckmtgfcimlii.us-east-2.rds.amazonaws.com'

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

############################First Graphic###############################

conn = psycopg2.connect( database=DB,user=USER,password=PASSWORD, host=HOST, port=PORT)

df_promedios=pd.read_sql("SELECT f.ruta_comercial, ROUND(AVG(f.num_buses),2) AS buses_dia,ROUND(AVG(num_pasajeros),2)  AS pasajeros_dia \
 FROM ( SELECT d.ruta_comercial,COUNT(d.vehiculo_id) as num_buses, SUM(d.cant_pasajeros) as num_pasajeros, d.dia \
 FROM ( SELECT ruta_comercial, vehiculo_id,EXTRACT(day from vd.fecha_trx) as dia, count(id_validacion) as cant_pasajeros \
FROM public.validacion vd \
INNER JOIN paradero_ruta p_r ON p_r.id_paradero_ruta=vd.paradero_ruta_id \
INNER JOIN ruta ON ruta.id_ruta=p_r.id_ruta \
WHERE  EXTRACT(month from fecha_trx)=4 \
GROUP BY ruta_comercial, vehiculo_id, dia \
) AS d \
GROUP BY d.ruta_comercial,d.dia \
	) AS f \
	GROUP BY f.ruta_comercial;",conn)


conn.close()


df_promedios["pasaj_x_bus_dia"] = round(df_promedios["pasajeros_dia"]/df_promedios["buses_dia"],2)
# print(df_promedios)

fig = px.scatter(df_promedios, x="pasajeros_dia", y="buses_dia", hover_data=["ruta_comercial"])

###########################Other Graphic########################
conn = psycopg2.connect( database=DB,user=USER,password=PASSWORD, host=HOST, port=PORT)

df_demand=pd.read_sql("SELECT fecha_trx, EXTRACT(hour from hora_trx) as hora, count(*) as pasajeros \
FROM public.validacion vd \
GROUP BY fecha_trx,hora;",conn)


conn.close()


fig2= px.scatter(df_demand, x="hora", y="pasajeros")


app.layout = html.Div(children=[
    html.H1(children='Correlation-One / DS4A Team',
            style={
            'textAlign': 'center'
            
        }),
    html.H4(children='Promedios de buses y pasajeros por dia',style={
            'textAlign': 'center'
            
        }),
    html.Div(children=[
        
        generate_table(df_promedios),
        
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        
     
    ], style={'columnCount': 2}),

    html.H4(children='Demanda de pasajeros por hora',style={
            'textAlign': 'center'
            
        }),

    
    
    dcc.Graph(
        id='example-graph2',
        figure=fig2
    )
])

# Start the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)
