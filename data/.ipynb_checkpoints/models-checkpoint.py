import pandas as pd
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





############################################graficos ####################################SELECT EXTRACT(day FROM fecha_trx)as day FROM

def scatter_numPasajeros_numBuses(month,ZoneValue,route):
    df_numPasajeros_numBuses=pd.read_sql(" \
    WITH filtro1 AS( \
       SELECT id_validacion , vehiculo_id, paradero_ruta_id,EXTRACT(day FROM fecha_trx)as dia, \
       CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_week FROM validacion \
       INNER JOIN operador ON operador.id_operador=validacion.operador_id \
       WHERE EXTRACT(month FROM fecha_trx) =" +"\'"+ month +"\'"+" AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
         \
       ), filtro2 AS( \
             SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta \
             INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta \
         \
         ), filtro3 AS(\
                 SELECT count(id_validacion)as numPasajeros1,filtro1.dia,vehiculo_id,filtro2.ruta_comercial, \
                 filtro1.day_week  FROM filtro1 \
                 INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id \
                 WHERE filtro2.ruta_comercial=" +"\'"+ route +"\'"+" \
                 GROUP BY  dia,vehiculo_id,filtro2.ruta_comercial,filtro1.day_week \
                ) \
    SELECT sum(numpasajeros1)as number_passengers_day, COUNT(vehiculo_id) as number_buses_day,  \
    dia as day , ruta_comercial as comertial_route,day_week  FROM filtro3 \
    GROUP BY dia,ruta_comercial,day_week;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_week']=df_numPasajeros_numBuses['day_week'].astype(str)
    df_numPasajeros_numBuses['day_week'].replace(dayWeek,inplace=True)
    df_numPasajeros_numBuses['day']=df_numPasajeros_numBuses['day'].astype(str)
    return df_numPasajeros_numBuses

def scatter_numPasajeros_numBuses_zonal(month,ZoneValue,route):
    df_numPasajeros_numBuses=pd.read_sql(" \
    WITH filtro1 AS( \
       SELECT id_validacion , vehiculo_id, paradero_ruta_id,EXTRACT(day FROM fecha_trx)as dia, \
       CAST(EXTRACT(dow FROM fecha_trx)AS INTEGER) AS day_week FROM validacion \
       INNER JOIN operador ON operador.id_operador=validacion.operador_id \
       WHERE EXTRACT(month FROM fecha_trx) =" +"\'"+ month +"\'"+" AND operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
         \
       ), filtro2 AS( \
             SELECT id_paradero_ruta, ruta.ruta_comercial FROM paradero_ruta \
             INNER JOIN ruta ON ruta.id_ruta=paradero_ruta.id_ruta \
         \
         ), filtro3 AS(\
                 SELECT count(id_validacion)as numPasajeros1,filtro1.dia,vehiculo_id,filtro2.ruta_comercial, \
                 filtro1.day_week  FROM filtro1 \
                 INNER JOIN filtro2 ON filtro2.id_paradero_ruta=filtro1.paradero_ruta_id \
                  \
                 GROUP BY  dia,vehiculo_id,filtro2.ruta_comercial,filtro1.day_week \
                ) \
    SELECT sum(numpasajeros1)as number_passengers_day, COUNT(vehiculo_id) as number_buses_day,  \
    dia as day , ruta_comercial as comertial_route,day_week  FROM filtro3 \
    GROUP BY dia,ruta_comercial,day_week;",connect_db.conn())

    connect_db.conn().close()
    dayWeek={'0':"sunday",'1':"monday",'2':"tuesday",'3':"wednesday",'4':"thursday",'5':"friday",'6':"saturday"}
    df_numPasajeros_numBuses['day_week']=df_numPasajeros_numBuses['day_week'].astype(str)
    df_numPasajeros_numBuses['day_week'].replace(dayWeek,inplace=True)
    df_numPasajeros_numBuses['day']=df_numPasajeros_numBuses['day'].astype(str)
    return df_numPasajeros_numBuses



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
  


