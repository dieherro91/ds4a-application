
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.cluster import KMeans
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
    connect_db.conn().Close()
    #Here we count how many routes pass by each stop:
    df_fe2 = df_fe2.groupby("cenefa").nunique("ruta_comercial").reset_index()
    df_fe2.rename(columns={'ruta_comercial':'cantidad_rutas'}, inplace=True)

    #Here we create 2 connectivity metrics. One using MinMaxScaling and the other one
    #applying log:
    min_value = df_fe2['cantidad_rutas'].min()
    max_value = df_fe2['cantidad_rutas'].max()
    df_fe2['connectivity_score'] = df_fe2['cantidad_rutas'].apply(lambda row: round(4 * (row - min_value)/(max_value - min_value)))
    df_fe2['connectivity_log_score'] = df_fe2['cantidad_rutas'].apply(lambda value: round(np.log(value)))
    
    return df_fe2

def df_validaciones(ZoneValue,route,start_date,end_date,a):

    df_validaciones = pd.read_sql("WITH validaciones AS (\
                            SELECT fecha_trx AS fecha_servicio, \
                            date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 60) * interval '1 minute') AS hora_servicio,\
                            paradero.id_paradero, \
                            ruta_comercial,\
                            cenefa, \
                            vehiculo_id, \
                            posicion,\
                            latitud,\
                            longitud\
                            FROM validacion\
                            JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
                            JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
                            JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
                            JOIN operador ON operador.id_operador = validacion.operador_id \
                            WHERE "+a+ range_date_postgreSQL(start_date,end_date) + " AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+"  \
                            )\
                            SELECT fecha_servicio, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion, latitud, longitud, count(*) AS cantidad_pasajeros\
                            FROM validaciones \
                            " + filtro_ruta1(route) +
                            "GROUP BY fecha_servicio, hora_servicio, ruta_comercial, cenefa, vehiculo_id, posicion, latitud, longitud\
                            ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC, posicion ASC;", connect_db.conn())
    connect_db.conn().Close()
    return df_validaciones


def pre_processing(df_validaciones):
    df_validaciones = df_validaciones.drop(columns=['posicion']).groupby(by = ['fecha_servicio','hora_servicio','cenefa']).sum().reset_index()
    ''' This function uses the input DataFrame and pre-process it to use it in a RandomForestRegressor.
    It adds the connectivity score feature, and it also adds to features of sine and cosine of the seconds of a certain moment of the day.
    '''
    # Primero se agregan los puntajes de conectividad
    df_fe2=auxiliar_prediction()
    df_validaciones_fe = df_validaciones.merge(df_fe2[['cenefa','cantidad_rutas','connectivity_score', 'connectivity_log_score']], left_on = 'cenefa', right_on = 'cenefa')

    #Creamos la categoría de mes y de día de la semana:
    df_validaciones_fe['mes'] =pd.to_datetime(df_validaciones_fe['fecha_servicio']).dt.month.astype('int')
    df_validaciones_fe['dia_semana'] = pd.to_datetime(df_validaciones_fe['fecha_servicio']).dt.weekday
    df_validaciones_fe['sin_dia_semana'] = np.sin(2*np.pi*(df_validaciones_fe['dia_semana']/7))
    df_validaciones_fe['cos_dia_semana'] = np.cos(2*np.pi*(df_validaciones_fe['dia_semana']/7))


    #Agregamos una columna que indique si un día es festivo o no:
    festivos = ['20210101', '20210106', '20210322', '20210401', '20210402', '20210501', '20210517', '20210607', '20210614', '20210705', '20210720', '20210807', '20210816', '20211018', '20211101', '20211115', '20211208', '20211225']
    df_validaciones_fe['es_festivo'] = df_validaciones_fe.fecha_servicio.astype(str).str.replace('-','').apply(lambda row: row in festivos).astype(int)


    #Realizamos One-hot encoding para las columnas categóricas que quizás usemos en el modelo:
    #df_validaciones_fe = pd.get_dummies(df_validaciones_fe, columns=['dia_semana'])
    #df_validaciones_fe = pd.get_dummies(df_validaciones_fe, columns=['dia_semana','cenefa'])


    #Transformamos la hora de servicio, para que sí tenga su característica cíclica (ejemplo: 23:55 está a 10 minutos de 00:05, no 23 horas y 50 minutos)
    df_validaciones_fe['seconds'] = df_validaciones_fe.hora_servicio.dt.seconds
    seconds_in_day = 24*60*60
    df_validaciones_fe['sin_time'] = np.sin(2*np.pi*df_validaciones_fe.seconds/seconds_in_day)
    df_validaciones_fe['cos_time'] = np.cos(2*np.pi*df_validaciones_fe.seconds/seconds_in_day) 
    df_validaciones_fe = df_validaciones_fe.sort_values(by=['fecha_servicio','hora_servicio']).reset_index(drop=True)

    return df_validaciones_fe

def df_reduced_1(ZoneValue,route,start_date,end_date,a):
    # union de las dos funciones para preprocesing
    return pre_processing(df_validaciones(ZoneValue,route,start_date,end_date,a))

def split_train_test(ZoneValue,route,start_date,end_date,a,test_size=0.2):
    df_reduced=df_reduced_1(ZoneValue,route,start_date,end_date,a)
    first_date = df_reduced['fecha_servicio'].min()
    final_date = df_reduced['fecha_servicio'].max()
    delta = final_date - first_date
    train_delta = (1- test_size) * delta
    final_train = first_date + train_delta

    df_train = df_reduced[df_reduced['fecha_servicio'] <= final_train]
    df_test = df_reduced[df_reduced['fecha_servicio'] > final_train]

    X_train = df_train.drop(columns = ['fecha_servicio','hora_servicio','ruta_comercial','vehiculo_id','latitud','longitud','cantidad_pasajeros','cantidad_rutas','connectivity_log_score','seconds','cenefa','dia_semana'])
    y_train = df_train[['cantidad_pasajeros']]

    X_test = df_test.drop(columns = ['fecha_servicio','hora_servicio','ruta_comercial','vehiculo_id','latitud','longitud','cantidad_pasajeros','cantidad_rutas','connectivity_log_score','seconds','cenefa','dia_semana'])
    y_test = df_test[['cantidad_pasajeros']]
    
    return X_train, X_test, y_train, y_test
    
###########################################   Cluster #################################

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137
    dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
    dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180) * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d * 1000

def data_frame_cluster(ZoneValue):
    df = pd.read_sql("SELECT ruta_comercial, paradero.id_paradero, count(id_validacion) as cant_pasajeros, \
                  posicion, latitud, longitud FROM public.validacion vd \
                  INNER JOIN paradero_ruta p_r ON p_r.id_paradero_ruta=vd.paradero_ruta_id \
                  INNER JOIN ruta ON ruta.id_ruta=p_r.id_ruta \
                  INNER JOIN paradero on paradero.id_paradero=p_r.id_paradero \
                  INNER JOIN operador ON operador.id_operador=vd.operador_id\
                  WHERE operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+"\
                  GROUP BY ruta_comercial, paradero.id_paradero, posicion, latitud, longitud \
                  ORDER BY ruta_comercial, posicion ASC;", connect_db.conn())
    connect_db.conn().close()

    df["dist"] = measure(df.latitud.shift(), df.longitud.shift(), df.loc[1:, 'latitud'], df.loc[1:, 'longitud'])
    df2= df.groupby("ruta_comercial", as_index=False).agg({"id_paradero": "count", "cant_pasajeros": "sum", "dist": "sum"})
    df2.rename(columns={'ruta_comercial':'route',
                        'id_paradero':'num_bus_stops',
                        'cant_pasajeros':'num_validations',
                        'dist':'length_bus_route'},
               inplace=True)
    return df2



