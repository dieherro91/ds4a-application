
#In this file are made the figures of the predictive app.

from data import models_prediction, list_training_data
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans


#Font use for the figures
family_font = 'KarlaMedium'
#########################################################################################################

################################################# cluster ##########################################
#This function return the cluster for all the routes for a given zone and the dataframe with the clusters 
def cluster(ZoneValue,n_clusters,route):
    df2=models_prediction.data_frame_cluster(ZoneValue)
    kmeans = KMeans(n_clusters=max(n_clusters, 1), algorithm='auto')
    kmeans.fit(df2[["length_bus_route", "num_bus_stops","num_validations"]])
    centers = kmeans.cluster_centers_
    df2['cluster'] = kmeans.labels_
    listen=[]
    for c in range(n_clusters):
        listen.append("Cluster {}".format(c))
    dictr={'length_bus_route':centers[:, 0],
            'num_bus_stops':centers[:, 1],
            'num_validations':centers[:,2],
            'cluster':listen}
    centros=pd.DataFrame(dictr)
    fig = px.scatter_3d(df2, x='num_bus_stops', y='length_bus_route',z='num_validations',
                            labels={"length_bus_route": "Distance (m)",
                                    "num_bus_stops": "number of buses",
                                    "num_validations": "number of passengers",
                                    },
                            hover_name='route',color='cluster',height=450)

    fig2=px.scatter_3d(centros,x='num_bus_stops',y='length_bus_route',z='num_validations',hover_name='cluster')
    fig.update_traces(marker_coloraxis=None)
    fig.update_layout(font=dict(family=family_font,color = 'black'),margin=dict(l=0, r=0, b=0, t=0))
    fig2.update_traces(marker_symbol='diamond',marker_color='black',marker={'size': 4})
    fig.add_trace(fig2.data[0])

    filter=df2[(df2['route']==route)].loc[:,'cluster'].values[0] 
    df_similar=df2[(df2['cluster']==filter)]
    df_similar.loc[:,'length_bus_route']=df_similar['length_bus_route'].round(decimals = 1)
    return fig, df_similar


#input_zona,input_ruta,input_date,strike=0
def map_street_predicted(ZoneValue,route,dates,strike):
    df=models_prediction.dataframe_prediction(ZoneValue,route,dates,strike)
    df_pred=df[['connectivity_score','order_cenefa','dia_semana','es_findesemana','semana',
   'es_festivo','paro','sin_time','cos_time','hora_pico','cantidad_pasajeros_shifted']].copy()
    list_output_predict=list_training_data.prediction_evaluation(df_pred,route)
    df['hora_servicio']=df['hora_servicio'].astype(int)
    df.insert(14,'passengers',list_output_predict,allow_duplicates=True)

    fig_scatter_mapbox = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="passengers",
                            size="passengers", animation_frame='hora_servicio',# animation_group="order_cenefa",
                            color_continuous_scale= ['#0000FF', '#00ff00','#ffff00 ', '#FF0000'],
                            zoom=11,height=500, mapbox_style='open-street-map', 
                            range_color=[0,df["passengers"].max()],
                            labels={'hora_servicio':'hour',
                                    'cenefa':'bus stop',
                                    'posicion':'Distance (m)'},
                            hover_name="cenefa", 
                            hover_data={
                            'latitud':False,
                            'longitud':False,
                            'cenefa':True,
                            'cenefa':'<b>cenefa<b>',
                            'hora_servicio':True,
                            'posicion':True,
                            'passengers':True,
                            'passengers':':.2f',
                            },
                          )
    fig_scatter_mapbox.update_layout(font=dict(family=family_font,color = 'black'))   
    
    fig_bar = px.bar(df, x='hora_servicio', y="passengers", color="passengers", 
        animation_frame="cenefa",range_color=[0,df["passengers"].max()],# animation_group="order_cenefa",
        range_y=[0,(df["passengers"].max()+1)],range_x=[3,24],hover_data=['cenefa','es_festivo','paro'],
        color_continuous_scale= ['#0000FF', '#00ff00','#ffff00 ', '#FF0000'],
        )
    fig_bar.update_layout(font=dict(family=family_font,color = 'black')) 

    animations = {
    'Map_street': fig_scatter_mapbox
    ,

    'Bar_hours': fig_bar,
                }

    
    return animations
