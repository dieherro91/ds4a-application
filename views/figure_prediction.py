
#In this file are made the figures of the predictive app.

from data import models_prediction
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans


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
    fig = px.scatter_3d(df2, x='length_bus_route', y='num_bus_stops',z='num_validations',
                            hover_name='route',color='cluster',height=350)

    fig2=px.scatter_3d(centros,x='length_bus_route',y='num_bus_stops',z='num_validations',hover_name='cluster')
    fig.update_traces(marker_coloraxis=None)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig2.update_traces(marker_symbol='diamond',marker_color='black',marker={'size': 4})
    fig.add_trace(fig2.data[0])

    filter=df2[(df2['route']==route)].loc[:,'cluster'].values[0] 
    df_similar=df2[(df2['cluster']==filter)]
    df_similar.loc[:,'length_bus_route']=df_similar['length_bus_route'].round(decimals = 1)
    return fig, df_similar