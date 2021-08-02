
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
        listRoutefinal.append({'label':df_name_buses['ruta_comercial'].loc[i],'value':df_name_buses['ruta_comercial'].loc[i]})
    
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





############################################Scatter ####################################SELECT EXTRACT(day FROM fecha_trx)as day FROM
def scatter_numPasajeros_numBuses_zonal(month,ZoneValue,route):
    df_numPasajeros_numBuses=pd.read_sql(" \
        WITH filtro1 AS(  \
           SELECT id_validacion , vehiculo_id, paradero_ruta_id,  \
           CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_of_week FROM validacion \
           INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
           WHERE CAST(EXTRACT(month FROM fecha_trx) AS INTEGER) = " +"\'"+ month +"\'"+"  AND \
                   operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
       ), filtro2 AS(  \
         SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta  \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta  \
         ), filtro3 AS(SELECT COUNT(id_validacion) AS validacion_pas , vehiculo_id ,day_of_week, filtro2.ruta_comercial FROM filtro1 \
                  INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
                    \
                  GROUP BY day_of_week,vehiculo_id,filtro2.ruta_comercial \
    )  \
    SELECT ROUND(AVG(validacion_pas),1) AS average_validations_per_bus ,COUNT(vehiculo_id) AS number_of_buses,  \
            day_of_week,ruta_comercial as commertial_route FROM filtro3 \
    GROUP BY day_of_week,ruta_comercial;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_of_week']=df_numPasajeros_numBuses['day_of_week'].astype(str)
    df_numPasajeros_numBuses['day_of_week'].replace(dayWeek,inplace=True)
    return df_numPasajeros_numBuses

def scatter_numPasajeros_numBuses_route(month,ZoneValue,route):
    df_numPasajeros_numBuses=pd.read_sql(" \
        WITH filtro1 AS(  \
           SELECT id_validacion , vehiculo_id, paradero_ruta_id,  \
           CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_of_week FROM validacion \
           INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
           WHERE CAST(EXTRACT(month FROM fecha_trx) AS INTEGER) = " +"\'"+ month +"\'"+"  AND \
                   operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+"     \
       ), filtro2 AS(  \
         SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta  \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta  \
         ), filtro3 AS(SELECT COUNT(id_validacion) AS validacion_pas , vehiculo_id ,day_of_week, filtro2.ruta_comercial FROM filtro1 \
                  INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
                  WHERE filtro2.ruta_comercial= " +"\'"+ route +"\'"+"  \
                  GROUP BY day_of_week,vehiculo_id,filtro2.ruta_comercial \
    )  \
    SELECT ROUND(AVG(validacion_pas),1) AS average_validations_per_bus ,COUNT(vehiculo_id) AS number_of_buses,  \
            day_of_week,ruta_comercial as commertial_route FROM filtro3 \
    GROUP BY day_of_week,ruta_comercial;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_of_week']=df_numPasajeros_numBuses['day_of_week'].astype(str)
    df_numPasajeros_numBuses['day_of_week'].replace(dayWeek,inplace=True)
    return df_numPasajeros_numBuses

def scatter_numPasajeros_numBuses_route_hour_weekday(month,ZoneValue,route,hour):
    df_numPasajeros_numBuses=pd.read_sql(" \
        WITH filtro1 AS(  \
           SELECT id_validacion , vehiculo_id, paradero_ruta_id,  \
           CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_of_week FROM validacion \
           INNER JOIN operador ON operador.id_operador=validacion.operador_id  \
           WHERE CAST(EXTRACT(month FROM fecha_trx) AS INTEGER) = " +"\'"+ month +"\'"+"  AND \
                   operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" AND \
                 CAST(EXTRACT(hour FROM hora_trx) AS INTEGER) = " +"\'"+ hour +"\'"+" \
       ), filtro2 AS(  \
         SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta  \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta  \
         ), filtro3 AS(SELECT COUNT(id_validacion) AS validacion_pas , vehiculo_id ,day_of_week, filtro2.ruta_comercial FROM filtro1 \
                  INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id  \
                  WHERE filtro2.ruta_comercial= " +"\'"+ route +"\'"+"  \
                  GROUP BY day_of_week,vehiculo_id,filtro2.ruta_comercial \
    )  \
    SELECT ROUND(AVG(validacion_pas),1) AS average_validations_per_bus ,COUNT(vehiculo_id) AS number_of_buses,  \
            day_of_week,ruta_comercial as commertial_route FROM filtro3 \
    GROUP BY day_of_week,ruta_comercial;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_of_week']=df_numPasajeros_numBuses['day_of_week'].astype(str)
    df_numPasajeros_numBuses['day_of_week'].replace(dayWeek,inplace=True)
    return df_numPasajeros_numBuses


################################################   MAP ##############################################################
def validaciones_ubication_zone_route(month,ZoneValue,route):
    
    df_validaciones_ubication_zone_route=pd.read_sql(" \
        WITH filtro1 AS( \
       SELECT id_validacion, paradero_ruta_id FROM validacion \
       INNER JOIN operador ON operador.id_operador=validacion.operador_id \
       WHERE EXTRACT(month FROM fecha_trx) =" +"\'"+ month +"\'"+" AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
         \
       ), filtro2 AS( \
         SELECT id_paradero_ruta ,id_paradero FROM paradero_ruta \
         INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta \
         WHERE ruta_comercial=" +"\'"+ route +"\'"+" \
     \
         ), filtro3 AS(SELECT id_paradero, filtro1.id_validacion FROM filtro2 \
         INNER JOIN filtro1 ON filtro1.paradero_ruta_id=filtro2.id_paradero_ruta \
     \
     ) \
    SELECT cenefa as border , latitud, longitud, COUNT(filtro3.id_validacion)as validations FROM paradero \
    INNER JOIN filtro3 ON filtro3.id_paradero=paradero.id_paradero \
    GROUP BY cenefa, latitud, longitud;",connect_db.conn())
    connect_db.conn().close()
    return df_validaciones_ubication_zone_route
  
################################################   histogram| ##############################################################
def histogram_validations(month,ZoneValue,route):
    df_demparaderos = pd.read_sql("WITH validaciones AS (\
    SELECT fecha_trx AS fecha_servicio, \
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
    WHERE EXTRACT(month FROM fecha_trx) =" +"\'"+ month +"\'"+" AND \
    operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
    )\
    SELECT descripcion_operador, fecha_servicio, hora_servicio, ruta_comercial, cenefa, \
    vehiculo_id, posicion, latitud, longitud, count(*) AS cantidad_pasajeros\
    FROM validaciones\
    WHERE validaciones.ruta_comercial=" +"\'"+ route +"\'"+" \
    GROUP BY fecha_servicio,descripcion_operador, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion, latitud, longitud\
    ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;",connect_db.conn())
    

    df_demparaderos['hora'] = df_demparaderos['hora_servicio'].dt.components.hours
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio'].dt.components.minutes
    df_demparaderos['hora_validacion'] = (pd.to_datetime(df_demparaderos['hora'].astype(str) + ':' + 
                                                         df_demparaderos['minutos'].astype(str), format='%H:%M'))
    df_demparaderos = df_demparaderos[['fecha_servicio', 'hora_validacion',
                                       'ruta_comercial', 'cenefa', 'vehiculo_id', 'posicion',
                                       'latitud', 'longitud', 'cantidad_pasajeros','hora','minutos']]
    df_demparaderos['fecha_servicio'] = pd.to_datetime(df_demparaderos['fecha_servicio'], format='%Y-%m-%d')
    df_ruta = df_demparaderos.copy()
    df_ruta.drop(columns=['ruta_comercial'], inplace=True)
    resultados = df_ruta.groupby(['fecha_servicio', 'vehiculo_id', 'hora_validacion', 'posicion',
                                  'cenefa'], as_index=False).agg({'cantidad_pasajeros': 'sum'})

    resultados['posicion_zero'] = 0
    resultados.loc[resultados['posicion'].eq(0.0),'posicion_zero']=1
    s = resultados.groupby(resultados['posicion_zero'].cumsum())['cantidad_pasajeros'].transform('sum')
    resultados['cumsum_demanda'] = np.where(resultados['posicion_zero'] == 1, s, 0)
    resultados_demanda = (resultados.loc[(resultados[['cumsum_demanda']] != 0).all(axis=1)])[['cumsum_demanda','fecha_servicio','hora_validacion']].reset_index()
    resultados_demanda.drop(['index'], axis=1, inplace=True)
    
    return resultados_demanda
########################################  heat_map #############################################################################
def heatmap_interctive(month,ZoneValue,route):
    df_demparaderos = pd.read_sql("WITH validaciones AS (\
    SELECT fecha_trx AS fecha_servicio, \
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
    WHERE EXTRACT(month FROM fecha_trx) =" +"\'"+ month +"\'"+" AND \
    operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
    )\
    SELECT descripcion_operador, fecha_servicio, hora_servicio, ruta_comercial, cenefa, \
    vehiculo_id, posicion, latitud, longitud, count(*) AS cantidad_pasajeros\
    FROM validaciones\
    WHERE validaciones.ruta_comercial=" +"\'"+ route +"\'"+" \
    GROUP BY fecha_servicio,descripcion_operador, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion, latitud, longitud\
    ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;",connect_db.conn())
    
    df_demparaderos['hora'] = df_demparaderos['hora_servicio'].dt.components.hours
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio'].dt.components.minutes
    df_demparaderos['hora_validacion'] = (pd.to_datetime(df_demparaderos['hora'].astype(str) + ':' + 
                                                         df_demparaderos['minutos'].astype(str), format='%H:%M'))
    df_demparaderos = df_demparaderos[['fecha_servicio', 'hora_validacion',
                                       'ruta_comercial', 'cenefa', 'vehiculo_id', 'posicion',
                                       'latitud', 'longitud', 'cantidad_pasajeros','hora','minutos']]
    df_demparaderos['fecha_servicio'] = pd.to_datetime(df_demparaderos['fecha_servicio'], format='%Y-%m-%d')
    df_ruta = df_demparaderos.copy()
    df_ruta.drop(columns=['ruta_comercial'], inplace=True)
    resultados = df_ruta.groupby(['fecha_servicio', 'vehiculo_id', 'hora_validacion', 'posicion',
                                  'cenefa'], as_index=False).agg({'cantidad_pasajeros': 'sum'})

    resultados['posicion_zero'] = 0
    resultados.loc[resultados['posicion'].eq(0.0),'posicion_zero']=1
    s = resultados.groupby(resultados['posicion_zero'].cumsum())['cantidad_pasajeros'].transform('sum')
    resultados['cumsum_demanda'] = np.where(resultados['posicion_zero'] == 1, s, 0)
    resultados_demanda = (resultados.loc[(resultados[['cumsum_demanda']] != 0).all(axis=1)])[['cumsum_demanda','fecha_servicio','hora_validacion']].reset_index()
    resultados_demanda.drop(['index'], axis=1, inplace=True)
    resultados['dia_semana'] = resultados['fecha_servicio'].dt.dayofweek
    resultados['hora'] = resultados['hora_validacion'].dt.hour
    dias_semana = {0:'Lunes',
               1:'Martes',
               2:'Miércoles',
               3:'Jueves',
               4:'Viernes',
               5:'Sábado',
               6:'Domingo'}
    resultados['nombre_dia'] = resultados.replace({'dia_semana':dias_semana})['dia_semana']
    resultados = resultados.sort_values(by='posicion')
    resultados['nombre_dia'] = resultados.replace({'dia_semana':dias_semana})['dia_semana']
    resultados = resultados.sort_values(by='posicion')
    return resultados


