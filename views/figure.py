from data import models_analysis
import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype
from sklearn.cluster import KMeans



family_font = 'Helvetica Neue'


#########################################################################################################

def graph1_validaciones_ubication_zone_route(start_date,end_date,ZoneValue,route,a):
    df=models_analysis.validaciones_ubication_zone_route(start_date,end_date,ZoneValue,route,a)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validations",hover_name="bus_stop", 
                            size="validations", 
                            color_continuous_scale= ['#0000FF', '#00ff00','#ffff00 ', '#FF0000'],
                            zoom=11,height=400, mapbox_style='open-street-map')
    if (route != ''):
        df2=models_analysis.position_route(ZoneValue,route)
        fig2= px.scatter_mapbox(df2 ,lat='latitude', lon='longitude',hover_data=['distance','bus_stop'])
        fig2.update_traces(marker_symbol='circle',marker_color='black')
        fig.add_trace(fig2.data[0])
    
    
    fig.update_layout(font=dict(family='Helvetica Neue',size=16,color = 'black',),
                    height=400,
                    margin=dict(autoexpand=True, l=0, r=0, t=40,b=0  ),
                    legend=dict(title='validation type',yanchor="top",y=0.99,xanchor="left",x=0.01,
                                    font =dict(family='Helvetica Neue',size=14,color = 'black',),
                                ),
                    )
    return fig 


#########################################################################################################
#SCATTER zonal
def make_graph_zonal(start_date,end_date,ZoneValue,route,a):
    df=models_analysis.scatter_numPasajeros_numBuses_zonal(start_date,end_date,ZoneValue,route,a)
    fig=px.scatter(df, y="average_validations_per_bus",x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week"], #animation_frame="validation_type",
                    height=400)
    fig.update_layout(font=dict(family=family_font,size=16,color = 'black',))
    return fig

#########################################################################################################
# average number buses route zonal 
def average_number_buses_per_day_per_month_zone_all_routes(start_date,end_date,ZoneValue,route,a):
    df=models_analysis.average_number_buses_per_day_per_month_zona_all_routes(start_date,end_date,ZoneValue,route,a)
    fig = px.bar(df, x='commertial_route', y='avg_num_bus_per_day', height=400 )
    fig.update_layout(font=dict(family='Sherif',size=16,color = 'black'),margin=dict(l=0,r=0,t=35,b=0))
    return fig

###########################################################################################################
def heat_map_interactivition(start_date,end_date,ZoneValue,route,a):
    resultados=models_analysis.heatmap_interctive(start_date,end_date,ZoneValue,route,a)
    cat_type = CategoricalDtype(categories=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    nbins_x=int(resultados['cenefa'].count())
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',z='cantidad_pasajeros',histfunc='sum',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Day name','hora':'Hour','cantidad_pasajeros':'valid.','cenefa':'bus stop'},
                            animation_frame='nombre_dia',
                            color_continuous_scale='reds',
                            category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y, nbinsx=nbins_x,height=400 ) 
    fig.update_layout(font=dict(family='Sherif',size=16,color = 'black'),margin=dict(l=0,r=0,t=35,b=0))
    fig.update_yaxes(autorange= 'reversed',nticks=8)
    fig.update_xaxes(tickangle=45,showticklabels=False)

    result=resultados.drop(columns=['fecha_servicio','hora_validacion',
                                    'posicion','posicion_zero','cumsum_demanda','dia_semana'])
    resulta=result.groupby(['cenefa','hora','nombre_dia']).sum().reset_index()
    fig_bar = px.bar(resulta, x="hora", y="cantidad_pasajeros",animation_frame="nombre_dia",hover_data=["cenefa"],
             labels={'nombre_dia':'Day name','hora':'Hour','cantidad_pasajeros':'Total validations','cenefa':'bus stop'},
             category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday']},
             height=400)
    fig_bar.update_layout(font=dict(family='Sherif',size=16,color = 'black'),margin=dict(l=0,r=0,t=35,b=0))
    return fig , fig_bar

############ bar plot average num bus per hour#########################################################
def average_number_buses_per_hour_route(start_date,end_date,ZoneValue,route,a):
    df=models_analysis.average_number_buses_per_hour_route(start_date,end_date,ZoneValue,route,a)
    fig = px.bar(df, x='hour', y='avg_num_bus', height=400 )
    fig.update_layout(font=dict(family='Sherif',size=16,color = 'black'),margin=dict(l=0,r=0,t=35,b=0))    
    return fig

#########################################################################################################
#HISTOGRAM
def histogram_validations(start_date,end_date,ZoneValue,route,a):
    resultados_demanda=models_analysis.histogram_validations(start_date,end_date,ZoneValue,route,a)
    fig=px.histogram(resultados_demanda, x='cumsum_demanda',labels={'cumsum_demanda':'Número de validaciones por viaje'},
                         height=400)
    fig.update_layout(xaxis_title_text = 'Number validations per ride', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(), annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout( margin=dict(l=0, r=10, t=28,b=0 ))
    fig.update_layout(font=dict(family='Sherif',size=16,color = 'black',))
    return fig

################################################# cluster ##########################################

def cluster(ZoneValue,n_clusters,route):
    df2=models_analysis.data_frame_cluster(ZoneValue)
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




