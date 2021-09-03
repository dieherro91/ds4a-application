
#In this file are all the queries and functions that is needed for the predictive page plots
import pandas as pd
import numpy as np
from pages import homes
from data import connect_db
import datetime

# measure function calculates the distance between bus stops
def measure(lat1, lon1, lat2, lon2):  
    R = 6378.137
    dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
    dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180) * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d * 1000

################################################# cluster ##########################################
#data_frame_cluster function orders the data from the data frame "homes.df_cluster" #
#which is obtained at the beginning of the page beacause is not depended for the users filters
def data_frame_cluster(ZoneValue):
    df_1=homes.df_cluster
    df=df_1[(df_1['zone']==ZoneValue)]
    df.drop(columns=['zone'])

    df["dist"] = measure(df.latitud.shift(), df.longitud.shift(), df.loc[1:, 'latitud'], df.loc[1:, 'longitud'])
    df2= df.groupby("ruta_comercial", as_index=False).agg({"id_paradero": "count", "cant_pasajeros": "sum", "dist": "sum"})
    df2.rename(columns={'ruta_comercial':'route',
                        'id_paradero':'num_bus_stops',
                        'cant_pasajeros':'num_validations',
                        'dist':'length_bus_route'},
               inplace=True)
    return df2

############################################################################################################


def get_info_stops_route(route,input_date):

    df_stops_route = pd.read_sql("SELECT DISTINCT cenefa,  min(posicion) as posicion, avg(latitud) as latitud, avg(longitud) as longitud FROM public.paradero_ruta AS par_ruta \
    INNER JOIN public.paradero AS par ON par_ruta.id_paradero=par.id_paradero \
    INNER JOIN public.ruta ON ruta.id_ruta=par_ruta.id_ruta \
    WHERE ruta.ruta_comercial = " +"\'"+ route +"\'"+" \
    GROUP BY cenefa \
    ORDER BY posicion ASC;", connect_db.conn())
    connect_db.conn().close()
    datet=input_date
    df_stops_route['date_pred'] = input_date

    return df_stops_route


def drop_extreme_values(df):
    "This function removes the rows that are part of 5 higher values"
    values = df['cantidad_pasajeros'].unique()
    maximum_values = sorted(values)[-5:]
    
    df_droped = df[~df['cantidad_pasajeros'].isin(maximum_values)]
    
    return df_droped

def sorted_cenefas(df):
    "This function sorted the bus stops by the maximum amount of passengers registered"
    "in the past months and the mean amount of passengers"

    cenefa_sorted_max = df.groupby('cenefa')['cantidad_pasajeros'].max().reset_index()
    cenefa_sorted_max = cenefa_sorted_max.rename(columns={"cantidad_pasajeros": "max"})
    
    cenefa_sorted_mean = df.groupby('cenefa')['cantidad_pasajeros'].mean().reset_index()
    cenefa_sorted_mean = cenefa_sorted_mean.rename(columns={"cantidad_pasajeros": "mean"})
    
    cenefa_sorted = cenefa_sorted_max.merge(cenefa_sorted_mean[['cenefa','mean']], left_on = 'cenefa', right_on = 'cenefa')
    
    cenefa_sorted['pasajeros'] = cenefa_sorted['max'] / cenefa_sorted['mean']
    
    cenefa_sorted = cenefa_sorted.sort_values(by = 'pasajeros').reset_index(drop = True)
    cenefa_sorted['order_cenefa'] = cenefa_sorted.index + 1 
    
    cenefa_sorted['pasajeros_round'] = np.round(cenefa_sorted['pasajeros'])
    
    return cenefa_sorted

def fe(df,df_conn,df_sorted):
   df = df.groupby(by = ['fecha_servicio','hora_servicio','cenefa'], as_index=False).agg({'cantidad_pasajeros': 'sum'})

   # Merging the new variables:
   df_fe = df.merge(df_conn[['cenefa','connectivity_score']], left_on = 'cenefa', right_on = 'cenefa')
   df_fe = df_fe.merge(df_sorted[['cenefa','order_cenefa']], left_on = 'cenefa', right_on = 'cenefa')  
   
   return df_fe

def rush_hours(df):
    df['hora'] = df['hora_servicio'].dt.seconds // 3600
    sorted_hours = df['hora'].value_counts().reset_index()
    rush_hours = sorted_hours['index'][0:6].tolist()
    
    return rush_hours

def pre_processing(df, peak_hours):
    ''' This function uses the input DataFrame and pre-process it to use it in a RandomForestRegressor.
    It adds the connectivity score feature, and it also adds to features of sine and cosine of the seconds of a certain moment of the day.
    '''
    
    # - Pre-processing of Date variable
    
    # df_validaciones_fe['mes'] = pd.to_datetime(df_validaciones_fe['fecha_servicio']).dt.month.astype('int')
    df['dia_semana'] = pd.to_datetime(df['fecha_servicio']).dt.weekday
    df['es_findesemana'] = df['dia_semana'].isin([5, 6]).astype(int)
    df['semana'] = pd.to_datetime(df['fecha_servicio']).dt.isocalendar().week.astype('int')
  
    # Holidays_variable:
    holidays = ['20210101', '20210106', '20210322', '20210401', '20210402', '20210501', '20210517', '20210607', '20210614',
                '20210705', '20210720', '20210807', '20210816', '20211018', '20211101', '20211115', '20211208', '20211225']
    df['es_festivo'] = df.fecha_servicio.astype(str).str.replace('-','').apply(lambda row: row in holidays).astype(int)
    
    # Protests variable:
    protests = ['20210427', '20210428', '20210429', '20210430', '20210501', '20210502', '20210503', '20210504', '20210505',
            '20210506', '20210507', '20210508', '20210509', '20210510', '20210511', '20210512', '20210513', '20210514',
            '20210515', '20210516', '20210704']
    df['paro'] = df.fecha_servicio.astype(str).str.replace('-','').apply(lambda row: row in protests).astype(int)

    
    # - Pre-processing of Time variable
    
    # We need to convert time in a cyclical variable 
    df['seconds'] = df.hora_servicio.dt.seconds
    seconds_in_day = 24*60*60
    df['sin_time'] = np.sin(2*np.pi*df['seconds']/seconds_in_day)
    df['cos_time'] = np.cos(2*np.pi*df['seconds']/seconds_in_day) 
    
    # Rush time variable
    df['hora_pico'] = (df['seconds'] // 3600).apply(lambda row: row in peak_hours).astype(int)
  
    # Ordering by date and time:
    df = df.sort_values(by=['fecha_servicio','hora_servicio', 'order_cenefa']).reset_index(drop=True)
    
    return df




#this function return a dataframe with the inputs necesaries for the prediction
def shifting(df):
    df = df.sort_values(by = ['order_cenefa','hora_servicio','dia_semana','semana'])
    pass_shifted = df[['cenefa','hora_servicio','dia_semana','cantidad_pasajeros']].groupby(['cenefa','hora_servicio',
                                                                                               'dia_semana']).shift()
    
    df_shift = df.join(pass_shifted, rsuffix = '_shifted')
    df_shift = df_shift.dropna()

    df_shift = df_shift.sort_values(by = ['fecha_servicio','hora_servicio']).reset_index(drop=True)
    
    return df_shift


def pre_processing_pred(df, peak_hours):  # tiene ligeros cambios con respecto a la funcion pre_processing
    ''' This function uses the input DataFrame and pre-process it to use it in a RandomForestRegressor.
    It adds the connectivity score feature, and it also adds to features of sine and cosine of the seconds of a certain moment of the day.
    '''
    
    # - Pre-processing of Date variable
    
    # df_validaciones_fe['mes'] = pd.to_datetime(df_validaciones_fe['fecha_servicio']).dt.month.astype('int')
    df['dia_semana'] = pd.to_datetime(df['fecha_servicio']).dt.weekday
    df['es_findesemana'] = df['dia_semana'].isin([5, 6]).astype(int)
    df['semana'] = pd.to_datetime(df['fecha_servicio']).dt.isocalendar().week.astype('int')

  
    # Holidays_variable:
    holidays = ['20210101', '20210106', '20210322', '20210401', '20210402', '20210501', '20210517', '20210607', '20210614',
                '20210705', '20210720', '20210807', '20210816', '20211018', '20211101', '20211115', '20211208', '20211225']
    df['es_festivo'] = df.fecha_servicio.astype(str).str.replace('-','').apply(lambda row: row in holidays).astype(int)
    
    # Protests variable:
    protests = ['20210427', '20210428', '20210429', '20210430', '20210501', '20210502', '20210503', '20210504', '20210505',
            '20210506', '20210507', '20210508', '20210509', '20210510', '20210511', '20210512', '20210513', '20210514',
            '20210515', '20210516', '20210704']
    df['paro'] = df.fecha_servicio.astype(str).str.replace('-','').apply(lambda row: row in protests).astype(int)

    
    # - Pre-processing of Time variable
    
    # We need to convert time in a cyclical variable 
    df['seconds'] = df['hora_servicio']*60*60
    seconds_in_day = 24*60*60
    df['sin_time'] = np.sin(2*np.pi*df['seconds']/seconds_in_day)
    df['cos_time'] = np.cos(2*np.pi*df['seconds']/seconds_in_day) 
    
    # # Rush time variable
    df['hora_pico'] = (df['seconds'] // 3600).apply(lambda row: row in peak_hours).astype(int)
    
    
    # Drop columns
    df = df.drop(columns = ['seconds']) 

    return df

def get_connectivity():
    
    df_conn = pd.read_sql("WITH stops AS (\
                                    SELECT ruta.ruta_sae, ruta.ruta_comercial, paradero.cenefa\
                                    FROM paradero_ruta \
                                    JOIN paradero ON paradero_ruta.id_paradero = paradero.id_paradero \
                                    JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta \
                                )\
                          SELECT * FROM stops", connect_db.conn())
    connect_db.conn().close()
    # Here we count how many routes pass by each stop:
    df_conn = df_conn.groupby("cenefa").nunique("ruta_comercial").reset_index()
    df_conn.rename(columns={'ruta_comercial':'cantidad_rutas'}, inplace=True)

    # Here we create 2 connectivity metrics. One using MinMaxScaling and the other one applying log:
    min_value = df_conn['cantidad_rutas'].min()
    max_value = df_conn['cantidad_rutas'].max()
    df_conn['connectivity_score'] = df_conn['cantidad_rutas'].apply(lambda row: round(4 * (row - min_value)/(max_value - min_value)))
    df_conn['connectivity_log_score'] = df_conn['cantidad_rutas'].apply(lambda value: round(np.log(value)))

    return df_conn

def get_validation_route(ZoneValue,route):
    df = pd.read_sql("WITH validaciones AS (\
                                SELECT fecha_trx AS fecha_servicio, \
                                date_trunc('minute', hora_trx)-((extract(minute FROM hora_trx)::integer % 60) * interval '1 minute') AS hora_servicio,\
                                paradero.id_paradero, \
                                ruta_comercial,\
                                cenefa, \
                                posicion \
                                FROM validacion\
                                JOIN paradero_ruta ON paradero_ruta.id_paradero_ruta = validacion.paradero_ruta_id \
                                JOIN ruta ON ruta.id_ruta = paradero_ruta.id_ruta\
                                JOIN paradero ON paradero.id_paradero = paradero_ruta.id_paradero\
                                JOIN operador ON operador.id_operador = validacion.operador_id \
                                WHERE operador.descripcion_operador=" +"\'"+ ZoneValue +"\'"+" \
                                )\
                                SELECT fecha_servicio, hora_servicio, ruta_comercial, cenefa, posicion, count(*) AS cantidad_pasajeros\
                                FROM validaciones\
                                WHERE validaciones.ruta_comercial=" +"\'"+ route +"\'"+" \
                                GROUP BY fecha_servicio, hora_servicio, ruta_comercial, cenefa, posicion\
                                ORDER BY fecha_servicio, ruta_comercial, hora_servicio ASC;", connect_db.conn())
    connect_db.conn().close()
    return df


def get_data_scheme(df_stops_route,valid_hours):
    data_X_pred = pd.DataFrame()
    data_temp = pd.DataFrame()
    for i in range(0,len(df_stops_route)):
      cenefa = df_stops_route['cenefa'][i]

      for j in range (0,len(valid_hours)):
        data_temp.loc[0,'hora_servicio']= valid_hours[j]
        data_temp.loc[0,'date_pred']= df_stops_route['date_pred'][i]
        data_temp.loc[0,'cenefa']= df_stops_route['cenefa'][i]
        data_temp.loc[0,'posicion']= df_stops_route['posicion'][i]
        data_temp.loc[0,'connectivity_score']= df_stops_route['connectivity_score'][i]
        data_temp.loc[0,'order_cenefa']= df_stops_route['order_cenefa'][i] 
        data_temp.loc[0,'latitud']= df_stops_route['latitud'][i] 
        data_temp.loc[0,'longitud']= df_stops_route['longitud'][i] 

        data_X_pred = data_X_pred.append(data_temp,ignore_index=True)

    data_X_pred['fecha_servicio'] = pd.to_datetime(data_X_pred['date_pred'])
    # data_X_pred

    return data_X_pred


def get_validation_day_before(df_shift, asu):

    dates_reg = pd.DataFrame()   #cargar data historica y filtrar los registros con el mismo dia (lun, mar, ..., etc) 
    dates_reg['fecha_servicio'] = df_shift['fecha_servicio']
    dates_reg['dia_semana'] = df_shift['dia_semana']
    dates_reg['hora_servicio'] = df_shift['hora_servicio']
    dates_reg['cenefa'] = df_shift['cenefa']
    dates_reg['cantidad_pasajeros'] = df_shift['cantidad_pasajeros']

    fecha_referencia = asu['fecha_servicio'][0]  # fecha ingresada por usuario pero en formato transformado registrado en el dataframe
    fechas_anteriores = dates_reg[dates_reg['fecha_servicio']<fecha_referencia]

    dia_semana_ref = asu['dia_semana'][0]

    fechas_anteriores_mismo_dia = fechas_anteriores[fechas_anteriores['dia_semana']==dia_semana_ref]
    fechas_anteriores_mismo_dia = fechas_anteriores_mismo_dia.reset_index()

    ref_last_day = fechas_anteriores_mismo_dia.tail(1)
    ref_last_day = ref_last_day['fecha_servicio'].item()
    ref_last_day   # fecha semana inmediatamente anterior

    registros_semana_anterior  = fechas_anteriores[fechas_anteriores['fecha_servicio']==ref_last_day]
    semana_anterior = registros_semana_anterior.drop(columns = ['fecha_servicio','dia_semana'])
    
    return semana_anterior





def dataframe_prediction(input_zona,input_ruta,input_date,strike):
    df_conn = homes.df_conectivity

    df = get_validation_route(input_zona,input_ruta)

    df_no_extreme = drop_extreme_values(df)
    df_sorted = sorted_cenefas(df_no_extreme)
    df_fe = fe(df,df_conn,df_sorted)
    peak_hours = rush_hours(df)
    df_pp = pre_processing(df_fe, peak_hours)
    df_shift = shifting(df_pp)
    df_shift['hora_servicio'] = df_shift['hora_servicio'].dt.components.hours


    df_stops_route = get_info_stops_route(input_ruta,input_date)

    info_cenefa = df_fe[['cenefa', 'connectivity_score', 'order_cenefa']]
    info_cenefa = info_cenefa.drop_duplicates()
    info_cenefa = info_cenefa.reset_index()
    info_cenefa = info_cenefa.drop(columns = ['index'])

    df_stops_route = df_stops_route.merge(info_cenefa, left_on = 'cenefa', right_on = 'cenefa') 


    valid_hours = list(range(4, 24, 1))

    data_X_pred = get_data_scheme(df_stops_route,valid_hours)

    asu = pre_processing_pred(data_X_pred, peak_hours)

    semana_anterior = get_validation_day_before(df_shift, asu)

    # cruce entre el dataframe del dia que se quiere predecir y el dataframe de los registros por paradero-hora de la semana anterior
    df_X_predictors = asu.merge(semana_anterior, how='left', left_on = ['cenefa','hora_servicio'], right_on = ['cenefa','hora_servicio'])

    df_X_predictors = df_X_predictors.drop(columns=['date_pred'])
    df_X_predictors.rename(columns={'cantidad_pasajeros':'cantidad_pasajeros_shifted', 'hora_servicio_x':'hora_servicio'}, inplace=True)
    df_X_predictors['cantidad_pasajeros_shifted'] = df_X_predictors['cantidad_pasajeros_shifted'].replace(np.nan, 0)
    if (strike==1):
        df_X_predictors['paro']=1

    
    return df_X_predictors
