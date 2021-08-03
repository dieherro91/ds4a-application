from data import models
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pandas.api.types import CategoricalDtype

def make_graph_route(month_scatter,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_zonal(month_scatter,ZoneValue,RouteValue)
    fig=px.scatter(df, x="number_passengers_day", y="number_buses_day", color="comertial_route",
                    hover_data=["day","comertial_route","day_week"],
                    
                    width=510, height=300)
    fig.update_layout(title='Validations vs number of buses per day week and validation type for {}'.format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ))
    
    
    #fig.layout.plot_bgcolor = '#4D7BC1'
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    return fig
#########################################################################################################
def make_graph_zonal(month_scatter,ZoneValue):
    df=models.scatter_numPasajeros_numBuses_zonal(month_scatter,ZoneValue)
    fig=px.scatter(df, y="average_validations_per_bus",x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week","validation_type"],
                    
                    width=510, height=300)
    fig.update_layout(title='Validations vs number of buses per day week and validation type for {}'.format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ))
    
    
    #fig.layout.plot_bgcolor = '#add19e'
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    
    return fig

def make_graph_route_single(month,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_route(month,ZoneValue,RouteValue)
    fig=px.scatter(df, y="average_validations_per_bus", x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week","validation_type"],
                    
                    width=510, height=300,)
    fig.update_layout(title='Validations vs number of buses per day week and validation type for {}'.format(RouteValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ))
    
    
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'

    return fig

def make_graph_route_single_hour(month,ZoneValue,RouteValue,hour):
    df=models.scatter_numPasajeros_numBuses_route_hour_weekday(month,ZoneValue,RouteValue,hour)
    fig=px.scatter(df, y="average_validations_per_bus", x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week","validation_type"],
                    title='Validations vs number of buses ({})'.format(RouteValue),
                    width=510, height=300,
                    template="plotly_dark")
    fig.update_layout(margin=dict(l=5, r=5, t=100, b=0))

    return fig
#########################################################################################################

def graph1_validaciones_ubication_zone(month,ZoneValue):
    df=models.validaciones_ubication_zone(month,ZoneValue)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validation_type",hover_name="bus_stop",
                            size="validations", zoom=11,height=400,width=600,)
    fig.update_layout(title="validations for {}".format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ),
                                
                                
                      margin=dict(autoexpand=True, l=0, r=0, t=50,b=0  ),
                      legend=dict(  title='validation type',
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    font =dict(
                                    family='Sherif',
                                    size=14,
                                    color = 'white',
                                    
                                                ),
                                ),
                       mapbox_style="open-street-map")
    
    fig.layout.plot_bgcolor = '#073559'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig 



def graph1_validaciones_ubication_zone_route(month,ZoneValue,route):
    df=models.validaciones_ubication_zone_route(month,ZoneValue,route)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validation_type",hover_name="bus_stop",
                            size="validations", zoom=11,height=400,width=600,)
    
    df2=models.position_route(month,ZoneValue,route)
    fig2= px.scatter_mapbox(df2 ,lat='latitude', lon='longitude', hover_data=['commertial_route','bus_stop','distance'])
    fig2.update_traces(marker_symbol='circle',marker_color='black')
    fig.add_trace(fig2.data[0])
    
    fig.update_layout(title="validations for {}".format(route),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ),
                                
                                
                      margin=dict(autoexpand=True, l=0, r=0, t=50,b=0  ),
                      legend=dict(  title='validation type',
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    font =dict(
                                    family='Sherif',
                                    size=14,
                                    color = 'white',
                                    
                                                ),
                                ),
                       mapbox_style="open-street-map")
    
    fig.layout.plot_bgcolor = '#073559'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig 

#########################################################################################################

def histogram_validations(month,ZoneValue,route):
    resultados_demanda=models.histogram_validations(month,ZoneValue,route)
    fig = px.histogram(resultados_demanda, x='cumsum_demanda', 
                    labels={'cumsum_demanda':'Número de validaciones por viaje'}
                   ,height=400,width=600)
    fig.update_layout(xaxis_title_text = 'Number validations per ride', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(),
              annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout( margin=dict(l=0, r=10, t=35,b=0 ))
    fig.update_layout(title='Histogram validations per travel route: {}'.format(route),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ))
    
    
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig

def histogram_validations_zone(month,ZoneValue):
    resultados_demanda=models.histogram_validations_zone(month,ZoneValue)
    fig = px.histogram(resultados_demanda, x='cumsum_demanda', 
                       labels={'cumsum_demanda':'Número de validaciones por viaje'},
                       height=400,width=600)
    fig.update_layout(xaxis_title_text = 'Number validations per ride', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(),
              annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout(margin=dict(l=0, r=10, t=35,b=0 ))
    fig.update_layout(title='Histogram validations per ride for all route, zone {}'.format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'white',                                    
                                    ))
    
    
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig

###########################################################################################################
def heat_map_interactivition(month,ZoneValue,route):
    resultados=models.heatmap_interctive(month,ZoneValue,route)
    
    cat_type = CategoricalDtype(categories=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Day name','hora':'Hour','count':'Total validations','cenefa':'bus stop'},
                            animation_frame='nombre_dia',
                            color_continuous_scale=["black",'#073559', "green"],
                            category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y,width=510, height=400 ) 
    fig.update_layout(title='Validations per hour by bus stop {}'.format(route),
                      font=dict(family='Sherif',size=16,color = 'white'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.update_yaxes(autorange= 'reversed',nticks=8)
    fig.update_xaxes(ticks='')
    fig.layout.paper_bgcolor = '#073559'

    return fig

def heat_map_interactivition_zone(month,ZoneValue):
    resultados=models.heatmap_interctive_zone(month,ZoneValue)
    
    cat_type = CategoricalDtype(categories=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Day name','hora':'Hour','count':'Total validations','cenefa':'bus stop'},
                            animation_frame='nombre_dia',
                            color_continuous_scale=["black", "green",'#073559'],
                            category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y,width=510, height=400)
    fig.update_layout(title='Validations per hour by bus stop {}'.format(ZoneValue),
                      font=dict(family='Sherif',size=16,color = 'white'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.update_yaxes(autorange= 'reversed',nticks=8)
    fig.update_xaxes(ticks='')
    fig.layout.paper_bgcolor = '#073559'

    return fig

##################################### BARRAS #########################################################

def average_number_buses_per_hour_zone(month,ZoneValue):
    df=models.average_number_buses_per_hour_zona(month,ZoneValue)
    fig = px.bar(df, x='hour', y='avg_num_bus',width=510, height=400 )
    
    fig.update_layout(title='Average quantity buses in a month for zone: {}'.format(ZoneValue),
                      font=dict(family='Sherif',size=16,color = 'white'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig

def average_number_buses_per_hour_route(month,ZoneValue,route):
    df=models.average_number_buses_per_hour_route(month,ZoneValue,route)
    fig = px.bar(df, x='hour', y='avg_num_bus',width=510, height=400 )
    
    fig.update_layout(title='Average quantity buses in a month for route: {}'.format(route),
                      font=dict(family='Sherif',size=16,color = 'white'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig
#########################################################################################################
def average_number_buses_per_day_per_month_zone_all_routes(month,ZoneValue):
    df=models.average_number_buses_per_day_per_month_zona_all_routes(month,ZoneValue)
    fig = px.bar(df, x='commertial_route', y='avg_num_bus_per_day',width=510, height=400 )
    fig.update_layout(title='Average quantity buses in a month per zone {}'.format(ZoneValue),
                      font=dict(family='Sherif',size=16,color = 'white'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.layout.plot_bgcolor = '#84A4D5'
    fig.layout.paper_bgcolor = '#073559'
    
    return fig