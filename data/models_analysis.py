
#In this file are all the queries that is needed for the analytic page plots

import pandas as pd
import numpy as np
from data import connect_db


################################################################################################
#################### funtions with the filters for the quearies #################################
################################################################################################
def exclude(listas):  # Exclude a list of dates given for the user in the analytic interface
    a=' '
    for item in listas:
        a= a + 'fecha_trx != '+"\'"+ item +"\'"+' AND '  
    return a

def range_date_postgreSQL(start_date,end_date): #Range of date given for the user in the analytic interface
    return 'fecha_trx >= '+"\'"+ start_date +"\'"+' AND fecha_trx <= '+"\'"+ end_date +"\'"+' '

########### 4 filters for the route given for the user in the analytic interface ################
def filtro_ruta1(route):
    if (route==' ' or route==''  ):
        return ' '
    return "WHERE validaciones.ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta2(route):
    if (route==' ' or route==''):
        return ' '
    return "WHERE filtro2.ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta3(route):
    if (route==' ' or route==''):
        return ' '
    return "WHERE ruta_comercial=" +"\'"+ route +"\' "
def filtro_ruta4(route):
    if (route==' ' or route==''):
        return ' '
    return "AND ruta_comercial=" +"\'"+ route +"\' "


################################################################################################
#################### funtions with the quearies neccesaries for plots ###########################
################################################################################################

##################Validations for the bus stop #################################################
#this function return a data frame with the number of validations with longitude and latitude
#with the filters and conditions given for the user in the interface page
#It will be used to make the map plot with the number of validations
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

############################Position of the bus stop #############################
#this function return a data frame with the longitude and latitude of buses stops
#with the filters and conditions given for the user in the interface page
#It will be used with the map plot for the number of validations 
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

###########Average validations per bus vs number of buses used per zone #################
#this function return a data frame with the number of validations per buses vs num buses 
#for all the zone and grouped by day of the week
#with the filters and conditions given for the user in the interface page
#It will be used to make the scatter plot
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

######################### Average number of buses per day used per zone ###############################
#this function return a data frame with the 15 routes for the with the average number of buses per day
#with the filters and conditions given for the user in the interface page
#It will be used to make the a bar plot
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

######################### Total validations for each bus stop and hour #############################
#this function return a data frame with the total validations for each bus stop and hour of the day
#with the filters and conditions given for the user in the interface page
#It will be used to make the a Heat map and a bar plot
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
        WHERE "+a+ range_date_postgreSQL(start_date,end_date) + " AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" )\
        SELECT fecha_servicio, hora_servicio, ruta_comercial, cenefa,vehiculo_id,  posicion, count(*) AS cantidad_pasajeros\
        FROM validaciones\
        "+filtro_ruta1(route)+
        "GROUP BY fecha_servicio, hora_servicio, ruta_comercial,vehiculo_id, cenefa,  posicion \
        ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;",connect_db.conn())
    connect_db.conn().close()
    dates_input = df_demparaderos['hora_servicio'].values.astype('datetime64[ns]')
    df_demparaderos['hora_servicio_aux']=pd.to_datetime(dates_input,format="%H:%M")
    df_demparaderos['hora'] = df_demparaderos['hora_servicio_aux'].dt.hour
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio_aux'].dt.minute
    df_demparaderos.drop(columns=['hora_servicio_aux'])
    df_demparaderos['hora_validacion'] = (pd.to_datetime(df_demparaderos['hora'].astype(str) + ':' + df_demparaderos['minutos'].astype(str), format='%H:%M'))

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

######################### average bus per hour #########################################
#this function return a data frame with average number of buses for each hour of the day
#with the filters and conditions given for the user in the interface page
#It will be used to make a bar plot
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


#########################validations per travel route ###########################
#this function return a data frame with validations per travel route
#with the filters and conditions given for the user in the interface page
#It will be used to make the a histogram plot
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
    dates_input = df_demparaderos['hora_servicio'].values.astype('datetime64[ns]')
    df_demparaderos['hora_servicio_aux']=pd.to_datetime(dates_input,format="%H:%M")
    df_demparaderos['hora'] = df_demparaderos['hora_servicio_aux'].dt.hour
    df_demparaderos['minutos'] = df_demparaderos['hora_servicio_aux'].dt.minute
    df_demparaderos.drop(columns=['hora_servicio_aux'])
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
