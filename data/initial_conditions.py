
#In this file the initial conditions is made to accelerate the dropdowns filters that not depend of a date
# also it make one searche for the clustering plot at the beginning of the page

from data import connect_db
import pandas as pd



################################################################################################
################################# DropDowns options needed #####################################
################################################################################################

def max_date():
    df_max_date=pd.read_sql("SELECT MAX(fecha_trx) FROM validacion",connect_db.conn())
    connect_db.conn().close()
    return df_max_date.iloc[0,0]

def min_date():
    df_min_date=pd.read_sql("SELECT MIN(fecha_trx) FROM validacion",connect_db.conn())
    connect_db.conn().close()
    return df_min_date.iloc[0,0]

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
    GROUP BY filtro2.ruta_comercial;",connect_db.conn())
    connect_db.conn().close()
    
    listRoutefinal=list()
    df_name_buses['ruta_comercial'].apply(str)
    for i in range(len(df_name_buses['ruta_comercial'])):
        values=df_name_buses['ruta_comercial'].loc[i]
        listRoutefinal.append({'label':values,'value':values})
    
    return listRoutefinal


################################################################################################
################################### clusterin initial information ##############################
################################################################################################

def data_frame_cluster():
    df = pd.read_sql("SELECT ruta_comercial, paradero.id_paradero, count(id_validacion) as cant_pasajeros, \
                  posicion, latitud, longitud,operador.descripcion_operador as zone FROM public.validacion vd \
                  INNER JOIN paradero_ruta p_r ON p_r.id_paradero_ruta=vd.paradero_ruta_id \
                  INNER JOIN ruta ON ruta.id_ruta=p_r.id_ruta \
                  INNER JOIN paradero on paradero.id_paradero=p_r.id_paradero \
                  INNER JOIN operador ON operador.id_operador=vd.operador_id\
                  \
                  GROUP BY ruta_comercial, paradero.id_paradero, posicion, \
                                            latitud, longitud,operador.descripcion_operador \
                  ORDER BY ruta_comercial, posicion ASC;", connect_db.conn())
    connect_db.conn().close()
    return df
