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


DB = 'masivo_sitp_2'
USER = 'postgres'
PORT =5432
PASSWORD = '4ng3lDS4A*83'
HOST='ds4a-83rds.ckmtgfcimlii.us-east-2.rds.amazonaws.com'

def average_1():
    
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
    
    return fig;

def demand_1():
    conn = psycopg2.connect( database=DB,user=USER,password=PASSWORD, host=HOST, port=PORT)

    df_demand=pd.read_sql("SELECT fecha_trx, EXTRACT(hour from hora_trx) as hora, count(*) as pasajeros \
    FROM public.validacion vd \
    GROUP BY fecha_trx,hora;",conn)


    conn.close()


    fig= px.scatter(df_demand, x="hora", y="pasajeros")
    return fig;

def heatmap_pasajeros():
    conn = psycopg2.connect( database=DB,user=USER,password=PASSWORD, host=HOST, port=PORT)
    df_paraderos = pd.read_sql("WITH validaciones AS (\
                                    SELECT fecha_trx AS fecha_servicio, extract(hour FROM validacion.hora_trx) AS hora_servicio, paradero.id_paradero, cenefa, pos_x, pos_y, latitud, longitud\
                                    FROM validacion\
                                    JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id\
                                    JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
                                ),\
                                demanda AS (\
                                    SELECT fecha_servicio, hora_servicio, cenefa, pos_x, pos_y, latitud, longitud, count(*) AS cantidad_pasajeros\
                                    FROM validaciones\
                                    GROUP BY fecha_servicio, hora_servicio, cenefa, pos_x, pos_y, latitud, longitud\
                                    ORDER BY fecha_servicio, hora_servicio ASC, cantidad_pasajeros DESC\
                                )\
                                SELECT max_dem_cenefa.fecha_servicio, max_dem_cenefa.hora_servicio, cenefa, pos_x, pos_y, latitud, longitud, cantidad_pasajeros\
                                FROM demanda AS demanda_total\
                                JOIN (\
                                    SELECT fecha_servicio, hora_servicio, MAX(cantidad_pasajeros) AS max_demanda\
                                    FROM demanda \
                                    GROUP BY fecha_servicio, hora_servicio) max_dem_cenefa\
                                ON max_dem_cenefa.fecha_servicio = demanda_total.fecha_servicio\
                                AND max_dem_cenefa.hora_servicio = demanda_total.hora_servicio\
                                AND max_dem_cenefa.max_demanda = demanda_total.cantidad_pasajeros",conn)
    conn.close()
    
    df_paraderos_tot = df_paraderos.groupby(["latitud", "longitud"]).sum().sort_values("cantidad_pasajeros").reset_index()
    
    fig = px.density_mapbox(df_paraderos_tot, lat='latitud', lon='longitud', z='cantidad_pasajeros', radius=10,
                        center=dict(lat=4.66, lon=-74.07), zoom=10, mapbox_style="stamen-terrain")
    return fig
