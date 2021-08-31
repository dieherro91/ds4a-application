
#In this file are all the queries and functions that is needed for the predictive page plots

import numpy as np
from pages import homes


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
#which is obtained at the begging of the page beacause is not depended for the users filters
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