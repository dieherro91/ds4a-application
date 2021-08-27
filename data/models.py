
import pandas as pd

import numpy as np
from data import connect_db


def listZone():    
    df_vehi_ope=pd.read_sql("SELECT descripcion_operador FROM operador;",connect_db.conn())    
    connect_db.conn().close()
    listZonefinal=list()
    
    df_vehi_ope['descripcion_operador'].apply(str)
    for i in range(len(df_vehi_ope['descripcion_operador'])):
        listZonefinal.append({'label':df_vehi_ope['descripcion_operador'].loc[i],'value':df_vehi_ope['descripcion_operador'].loc[i]})

    return listZonefinal

def ruta_comercial(ZoneValue):
    df_name_buses=pd.read_sql("WITH filtro1 AS(\
    SELECT operador.descripcion_operador, validacion.paradero_ruta_id FROM operador\
    INNER JOIN validacion ON validacion.operador_id=operador.id_operador\
    WHERE operador.descripcion_operador= " +"\'"+ ZoneValue +"\'"+" \
    GROUP BY operador.descripcion_operador,validacion.paradero_ruta_id\
    ), filtro2 AS(\
    SELECT ruta.ruta_comercial,paradero_ruta.id_paradero_ruta FROM ruta\
    INNER JOIN paradero_ruta ON paradero_ruta.id_ruta=ruta.id_ruta\
    GROUP BY ruta.ruta_comercial,paradero_ruta.id_paradero_ruta\
    )\
    SELECT filtro2.ruta_comercial FROM filtro2\
    INNER JOIN filtro1 ON filtro1.paradero_ruta_id=filtro2.id_paradero_ruta\
    GROUP BY filtro2.ruta_comercial\
    LIMIT(20);",connect_db.conn())
    connect_db.conn().close()
    
    listRoutefinal=list()
    
    df_name_buses['ruta_comercial'].apply(str)
    for i in range(len(df_name_buses['ruta_comercial'])):
        values=df_name_buses['ruta_comercial'].loc[i]
        listRoutefinal.append({'label':values,'value':values})
    
    return listRoutefinal

def month():
    df_month=pd.read_sql("SELECT CAST(EXTRACT(month FROM fecha_trx) AS INTEGER) as month  FROM validacion \
    GROUP BY month;",connect_db.conn())
    connect_db.conn().close()   
    df_month['month']=df_month['month'].astype(str)  
    month_list=list()
    for i in range(len(df_month['month'])):
        month_list.append({'label':df_month['month'].loc[i],'value':df_month['month'].loc[i]})
    return month_list

def day():
    df_day=pd.read_sql(" SELECT EXTRACT(day FROM fecha_trx)as day FROM validacion \
    GROUP BY day;",connect_db.conn())
    connect_db.conn().close()
    df_day['day']=df_day['day'].astype(str)
    day_list=list()
    for i in range(len(df_day['day'])):
        day_list.append({'label':df_day['day'].loc[i],'value':df_day['day'].loc[i]}) 
    return day_list

def max_date():
    df_max_date=pd.read_sql("SELECT MAX(fecha_trx) FROM validacion",connect_db.conn())
    connect_db.conn().close()
    return df_max_date.iloc[0,0]

def min_date():
    df_min_date=pd.read_sql("SELECT MIN(fecha_trx) FROM validacion",connect_db.conn())
    connect_db.conn().close()
    return df_min_date.iloc[0,0]
#month = start_date,end_date



def exclude(listas):
    a=' '
    for item in listas:
        a= a + 'fecha_trx != '+"\'"+ item +"\'"+' AND '
        
    return a
######################################################filters for dataBase #######################
def range_date_postgreSQL(start_date,end_date):
    return 'fecha_trx >= '+"\'"+ start_date +"\'"+' AND fecha_trx <= '+"\'"+ end_date +"\'"+' '

def filtro_ruta1(route):
    if (route==' '):
        return ' '
    return "WHERE validaciones.ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta2(route):
    if (route==' '):
        return ' '
    return "WHERE filtro2.ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta3(route):
    if (route==' '):
        return ' '
    return "WHERE ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta4(route):
    if (route==' '):
        return ' '
    return "AND ruta_comercial=" +"\'"+ route +"\' "
##################################################################################################################
"""
def verificacion_fechas(start_date,end_date,ZoneValue,route,a): ##################################################
    df_demparaderos = pd.read_sql(" \
        SELECT DISTINCT date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 5) * interval '1 minute') AS \
                                                                hora_servicio FROM validacion\
        JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
        JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
        JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
        JOIN operador ON operador.id_operador = validacion.operador_id \
        WHERE "+a+ range_date_postgreSQL(start_date,end_date) + "AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" AND \
                                                                        ruta_comercial= " +"\'"+ route +"\'"+" ;",connect_db.conn())
    connect_db.conn().close()
    
    return df_demparaderos['hora_servicio'].dt.components.days
"""
################################################   MAP ##############################################################
def validaciones_ubication_zone_route(start_date,end_date,ZoneValue,route,a):
    df_validaciones_ubication_zone_route=pd.read_sql(" \
        WITH filtro1 AS( \
       SELECT id_validacion, paradero_ruta_id FROM validacion \
       INNER JOIN operador ON operador.id_operador=validacion.operador_id \
       INNER JOIN tipo_viaje ON tipo_viaje.id_tipo_viaje=validacion.tipo_viaje_id \
       WHERE "+a+ range_date_postgreSQL(start_date,end_date) + " AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
         \
       ), filtro2 AS( \
         SELECT id_paradero_ruta ,id_paradero FROM paradero_ruta \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta \
         "+filtro_ruta3(route)+
         "), filtro3 AS(SELECT id_paradero, filtro1.id_validacion  FROM filtro2 \
         INNER JOIN filtro1 ON filtro1.paradero_ruta_id=filtro2.id_paradero_ruta \
     \
     ) \
    SELECT cenefa as bus_stop , latitud, longitud, COUNT(filtro3.id_validacion)as validations \
                                                                FROM paradero \
    INNER JOIN filtro3 ON filtro3.id_paradero=paradero.id_paradero \
    GROUP BY cenefa, latitud, longitud;",connect_db.conn())
    connect_db.conn().close()
    return df_validaciones_ubication_zone_route

def position_route(ZoneValue,route):
    df_estaciones=pd.read_sql(" \
    SELECT DISTINCT ruta_comercial as commertial_route, \
                              cenefa as bus_stop, latitud AS latitude, longitud AS longitude, posicion AS distance, \
                                descripcion_operador FROM public.validacion vd \
                                  \
    INNER JOIN paradero_ruta p_r ON p_r.id_paradero_ruta=vd.paradero_ruta_id \
    INNER JOIN ruta ON ruta.id_ruta=p_r.id_ruta \
    INNER JOIN paradero ON paradero.id_paradero=p_r.id_paradero \
    INNER JOIN operador ON operador.id_operador = vd.operador_id \
    WHERE operador.descripcion_operador= " +"\'"+ ZoneValue +"\'" +" "+ filtro_ruta4(route) +"   \
    ORDER BY posicion;",connect_db.conn())
    connect_db.conn().close()
    return df_estaciones


############################################Scatter ####################################SELECT EXTRACT(day FROM fecha_trx)as day FROM
def scatter_numPasajeros_numBuses_zonal(start_date,end_date,ZoneValue,route,a):
    df_numPasajeros_numBuses=pd.read_sql(" \
        WITH filtro1 AS(  \
           SELECT id_validacion , vehiculo_id, paradero_ruta_id,  \
           CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_of_week FROM validacion \
           INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
           INNER JOIN tipo_viaje ON tipo_viaje.id_tipo_viaje=validacion.tipo_viaje_id \
           WHERE "+ a + range_date_postgreSQL(start_date,end_date) + "  AND \
                   operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+"     \
       ), filtro2 AS(  \
         SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta  \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta  \
         ), filtro3 AS(SELECT COUNT(id_validacion) AS validacion_pas , vehiculo_id ,day_of_week, \
                 filtro2.ruta_comercial FROM filtro1 \
                  INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
                  "+filtro_ruta2(route)+  
                  "GROUP BY day_of_week,vehiculo_id,filtro2.ruta_comercial \
    )  \
    SELECT ROUND(AVG(validacion_pas),1) AS average_validations_per_bus ,COUNT(vehiculo_id) AS number_of_buses,  \
            day_of_week,ruta_comercial as commertial_route FROM filtro3 \
    GROUP BY day_of_week,ruta_comercial ;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_of_week']=df_numPasajeros_numBuses['day_of_week'].astype(str)
    df_numPasajeros_numBuses['day_of_week'].replace(dayWeek,inplace=True)
    return df_numPasajeros_numBuses

########################################## average buses zone ##############################################
def average_number_buses_per_day_per_month_zona_all_routes(start_date,end_date,ZoneValue,route,a):
    
    df_average_number_buses_per_day_per_month_zona = pd.read_sql(" \
    WITH filtro1 AS(  \
        SELECT id_validacion , vehiculo_id, paradero_ruta_id,  \
        CAST(EXTRACT(day FROM fecha_trx)AS INTEGER) AS day  FROM validacion \
        INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
        INNER JOIN tipo_viaje ON tipo_viaje.id_tipo_viaje = validacion.tipo_viaje_id \
        WHERE "+a+ range_date_postgreSQL(start_date,end_date) + "  \
        AND operador.descripcion_operador= "+"\'"+ ZoneValue +"\'"+" \
        \
        ), filtro2 AS(  \
        SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta  \
        INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta  \
        ), filtro3 AS(SELECT  vehiculo_id ,day, filtro2.ruta_comercial, COUNT(id_validacion)  FROM filtro1 \
        INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
        "+filtro_ruta2(route)+
        "GROUP BY vehiculo_id, day ,ruta_comercial \
        ) ,filtro4 AS(SELECT COUNT(vehiculo_id) AS num_buses ,ruta_comercial,day FROM filtro3 \
        GROUP BY day ,ruta_comercial \
        ) \
        SELECT ROUND(AVG(num_buses),2)as avg_num_bus_per_day,ruta_comercial AS commertial_route FROM filtro4 \
        ruta_comercial \
        GROUP BY ruta_comercial \
        ORDER BY avg_num_bus_per_day DESC \
        LIMIT (15);",connect_db.conn())
    connect_db.conn().close()
    
    return df_average_number_buses_per_day_per_month_zona

########################################  heat_map and bar validations ####################################################
def heatmap_interctive(start_date,end_date,ZoneValue,route,a):
    df_demparaderos = pd.read_sql("WITH validaciones AS (\
        SELECT fecha_trx AS fecha_servicio, \
        date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 5) * interval '1 minute') AS hora_servicio,\
        paradero.id_paradero, \
        ruta_comercial,\
        cenefa, \
        vehiculo_id, \
        posicion \
        FROM validacion\
        JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
        JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
        JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
        JOIN operador ON operador.id_operador = validacion.operador_id \
        WHERE "+a+ range_date_postgreSQL(start_date,end_date) + " AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
        )\
        SELECT fecha_servicio, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion, count(*) AS cantidad_pasajeros\
        FROM validaciones\
        "+filtro_ruta1(route)+
        "GROUP BY fecha_servicio, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion \
        ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;",connect_db.conn())
    connect_db.conn().close()
    
    df_demparaderos['hora'] = df_demparaderos['hora_servicio'].dt.components.hours
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio'].dt.components.minutes
    df_demparaderos['hora_validacion'] = (pd.to_datetime(df_demparaderos['hora'].astype(str) + ':' +       df_demparaderos['minutos'].astype(str), format='%H:%M'))

    df_demparaderos = df_demparaderos[['fecha_servicio', 'hora_validacion', 
                                       'cenefa', 'vehiculo_id', 'posicion', 'cantidad_pasajeros','hora','minutos']]
    df_demparaderos['fecha_servicio'] = pd.to_datetime(df_demparaderos['fecha_servicio'], format='%Y-%m-%d')


    resultados = df_demparaderos.groupby(['fecha_servicio', 'vehiculo_id',
                                          'hora_validacion', 'posicion', 'cenefa'], as_index=False).agg({'cantidad_pasajeros': 'sum'})

    resultados['posicion_zero'] = 0
    resultados.loc[resultados['posicion'].eq(0.0),'posicion_zero']=1
    s = resultados.groupby(resultados['posicion_zero'].cumsum())['cantidad_pasajeros'].transform('sum')
    resultados['cumsum_demanda'] = np.where(resultados['posicion_zero'] == 1, s, 0)

    resultados['dia_semana'] = resultados['fecha_servicio'].dt.dayofweek

    resultados['hora'] = resultados['hora_validacion'].dt.hour
    
    dias_semana = {0:'monday',
               1:'tuesday',
               2:'wednesday',
               3:'thursday',
               4:'friday',
               5:'saturday',
               6:'sunday'}
    resultados['nombre_dia'] = resultados.replace({'dia_semana':dias_semana})['dia_semana']
    resultados = resultados.sort_values(by='posicion')
    resultados['nombre_dia'] = resultados.replace({'dia_semana':dias_semana})['dia_semana']
    resultados = resultados.sort_values(by='posicion')
    return resultados

######################### average buss per hour ######################################################
def average_number_buses_per_hour_route(start_date,end_date,ZoneValue,route,a):
    df_average_number_buses_per_hour = pd.read_sql(" \
        WITH filtro1 AS(  \
       SELECT DISTINCT vehiculo_id, CAST(EXTRACT(day FROM fecha_trx)AS INTEGER) AS day, \
                         paradero_ruta_id,CAST(EXTRACT(hour FROM hora_trx)AS INTEGER) AS hour  FROM validacion \
       INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
       WHERE "+a+ range_date_postgreSQL(start_date,end_date) + "  \
               AND operador.descripcion_operador= "+"\'"+ ZoneValue +"\'"+"  \
       ), filtro2 AS(   \
         SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta   \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta   \
       \
         ), filtro3 AS(SELECT  day, hour, COUNT(filtro1.vehiculo_id) as number_buses FROM filtro1  \
                  INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
                  "+ filtro_ruta2(route)+
                  " GROUP BY day ,hour  \
          )  \
    SELECT ROUND(AVG(number_buses),2)as avg_num_bus,hour FROM filtro3  \
      \
    GROUP BY hour  \
    ORDER BY hour ASC;",connect_db.conn())
    connect_db.conn().close()
    return df_average_number_buses_per_hour


################################################   histogram| ##############################################################
def histogram_validations(start_date,end_date,ZoneValue,route,a):
    df_demparaderos = pd.read_sql("WITH validaciones AS (\
        SELECT fecha_trx AS fecha_servicio, \
        date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 5) * interval '1 minute') AS hora_servicio,\
        paradero.id_paradero, \
        ruta_comercial,\
        cenefa, \
        vehiculo_id, \
        posicion\
        FROM validacion\
        JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
        JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
        JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
        JOIN operador ON operador.id_operador = validacion.operador_id \
        WHERE "+a+ range_date_postgreSQL(start_date,end_date) + " AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
        )\
        SELECT fecha_servicio, hora_servicio, cenefa, vehiculo_id, posicion, count(*) AS cantidad_pasajeros\
        FROM validaciones\
        "+filtro_ruta1(route)+
        "GROUP BY fecha_servicio, hora_servicio, cenefa, vehiculo_id, posicion\
        ORDER BY fecha_servicio, hora_servicio ASC, posicion ASC;",connect_db.conn())
    connect_db.conn().close()
    
    df_demparaderos['hora'] = df_demparaderos['hora_servicio'].dt.components.hours
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio'].dt.components.minutes
    df_demparaderos['hora_validacion'] = (pd.to_datetime(df_demparaderos['hora'].astype(str) + ':' + 
                                                         df_demparaderos['minutos'].astype(str), format='%H:%M'))
    df_demparaderos = df_demparaderos[['fecha_servicio', 'hora_validacion', 'cenefa',
                                               'vehiculo_id', 'posicion', 'cantidad_pasajeros','hora','minutos']]
    df_demparaderos['fecha_servicio'] = pd.to_datetime(df_demparaderos['fecha_servicio'], format='%Y-%m-%d')
    
    
    resultados = df_demparaderos.groupby(['fecha_servicio', 'vehiculo_id', 'hora_validacion', 
                                              'posicion', 'cenefa'], as_index=False).agg({'cantidad_pasajeros': 'sum'})

    resultados['posicion_zero'] = 0
    resultados.loc[resultados['posicion'].eq(0.0),'posicion_zero']=1
    s = resultados.groupby(resultados['posicion_zero'].cumsum())['cantidad_pasajeros'].transform('sum')
    resultados['cumsum_demanda'] = np.where(resultados['posicion_zero'] == 1, s, 0)
    
    resultados_demanda = (resultados.loc[(resultados[['cumsum_demanda']] != 0).all(axis=1)])[['cumsum_demanda','fecha_servicio','hora_validacion']].reset_index()
    resultados_demanda.drop(['index'], axis=1, inplace=True)
    
    return resultados_demanda


#################################################### prediction ##################################



def auxiliar_prediction():
    df_fe2 = pd.read_sql("WITH stops AS (\
                                SELECT ruta.ruta_sae, ruta.ruta_comercial, paradero.cenefa\
                                FROM paradero_ruta \
                                JOIN paradero ON paradero_ruta.id_paradero = paradero.id_paradero \
                                JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta \
                             )\
                       SELECT * FROM stops", connect_db.conn())
    connect_db.conn().close()
    #Here we count how many routes pass by each stop:
    df_fe2 = df_fe2.groupby("cenefa").nunique("ruta_comercial").reset_index()
    df_fe2.rename(columns={'ruta_comercial':'cantidad_rutas'}, inplace=True)

    #Here we create 2 connectivity metrics. One using MinMaxScaling and the other one
    #applying log:
    min_value = df_fe2['cantidad_rutas'].min()
    max_value = df_fe2['cantidad_rutas'].max()
    df_fe2['connectivity_score'] = df_fe2['cantidad_rutas'].apply(lambda row: round(4 * (row - min_value)/(max_value - min_value)))
    df_fe2['connectivity_log_score'] = df_fe2['cantidad_rutas'].apply(lambda value: round(np.log(value)))
    df_fe2.sort_values(by=['connectivity_score'], ascending=False)  
    return df_fe2

