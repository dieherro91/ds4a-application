from data import models
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pandas.api.types import CategoricalDtype

family_font = 'Helvetica Neue'



def make_graph_route(start_date,end_date,ZoneValue,RouteValue,a):
    df=models.scatter_numPasajeros_numBuses_zonal(start_date,end_date,ZoneValue,RouteValue,a)
    fig=px.scatter(df, x="number_passengers_day", y="number_buses_day", color="comertial_route",
                    hover_data=["comertial_route","day_week",],  #animation_frame=["validation_type"],
                    
                    width=510, height=400)
    fig.update_layout(title='Avg validations vs # buses for {}'.format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ))
    
    
    #fig.layout.plot_bgcolor = '#4D7BC1'
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    return fig
#########################################################################################################
def make_graph_zonal(start_date,end_date,ZoneValue,a):
    df=models.scatter_numPasajeros_numBuses_zonal(start_date,end_date,ZoneValue,a)
    fig=px.scatter(df, y="average_validations_per_bus",x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week"], #animation_frame="validation_type",
                    height=400)
    fig.update_layout(
                                font=dict(
                                    family=family_font,
                                    size=16,
                                    color = 'black',                                    
                                    ))
                                    # title='Validations vs number of buses per day week for {}'.format(ZoneValue),
    
    
    #fig.layout.plot_bgcolor = '#add19e'
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    
    return fig

def make_graph_route_single(start_date,end_date,ZoneValue,RouteValue,a):
    df=models.scatter_numPasajeros_numBuses_route(start_date,end_date,ZoneValue,RouteValue,a)
    fig=px.scatter(df, y="average_validations_per_bus", x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","validation_type"],    #    animation_frame="validation_type",
                    
                    width=510, height=400,)
    fig.update_layout(title='Avg validations vs # buses for {}'.format(RouteValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ))
    
    
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'

    return fig

def make_graph_route_single_hour(start_date,end_date,ZoneValue,RouteValue,hour,a):
    df=models.scatter_numPasajeros_numBuses_route_hour_weekday(start_date,end_date,ZoneValue,RouteValue,hour,a)
    fig=px.scatter(df, y="average_validations_per_bus", x="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week","validation_type"],animation_frame="validation_type",
                    title='Avg validations vs # buses for ({})'.format(RouteValue),
                    width=510, height=400,
                    template="plotly_dark")
    fig.update_layout(margin=dict(l=5, r=5, t=100, b=0))

    return fig
#########################################################################################################

def graph1_validaciones_ubication_zone(start_date,end_date,ZoneValue,a):
    df=models.validaciones_ubication_zone(start_date,end_date,ZoneValue,a)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validations",hover_name="bus_stop", size="validations",
                            color_continuous_scale= ['#0000FF', '#00ff00','#ffff00 ', '#FF0000'],
                            zoom=11,height=400,)
    fig.update_layout(title="validations between {} / {} for {}".format(start_date,end_date,ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ),
                                
                                
                      margin=dict(autoexpand=True, l=0, r=0, t=40,b=0  ),
                      legend=dict(  title='validation type',
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    font =dict(
                                    family='Helvetica Neue',
                                    size=14,
                                    color = 'black',
                                    
                                                ),
                                ),
                       mapbox_style="open-street-map")
    
    #fig.layout.plot_bgcolor = '#073559'
    #fig.layout.paper_bgcolor = color_offwhite
    
    return fig 



def graph1_validaciones_ubication_zone_route(start_date,end_date,ZoneValue,route,a):
    df=models.validaciones_ubication_zone_route(start_date,end_date,ZoneValue,route,a)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validations",hover_name="bus_stop", size="validations", 
                            color_continuous_scale= ['#0000FF', '#00ff00','#ffff00 ', '#FF0000'],
                            zoom=11,height=400,)
    
    df2=models.position_route(ZoneValue,route)
    fig2= px.scatter_mapbox(df2 ,lat='latitude', lon='longitude', hover_data=['commertial_route','bus_stop','distance'])
    fig2.update_traces(marker_symbol='circle',marker_color='black')
    fig.add_trace(fig2.data[0])
    
    fig.update_layout(title="validations between {} / {} for {} in {}".format(start_date,end_date,route,ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ),
                                
                                
                      margin=dict(autoexpand=True, l=0, r=0, t=40,b=0  ),
                      legend=dict(  title='validation type',
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    font =dict(
                                    family='Helvetica Neue',
                                    size=14,
                                    color = 'black',
                                    
                                                ),
                                ),
                       mapbox_style="open-street-map")
    
    #fig.layout.plot_bgcolor = '#073559'
    #fig.layout.paper_bgcolor = '#073559'
    
    return fig 

#########################################################################################################

def histogram_validations(start_date,end_date,ZoneValue,route,a):
    resultados_demanda=models.histogram_validations(start_date,end_date,ZoneValue,route,a)
    fig = px.histogram(resultados_demanda, x='cumsum_demanda', 
                    labels={'cumsum_demanda':'Número de validaciones por viaje'}, height=400)
    fig.update_layout(xaxis_title_text = 'Number validations per ride', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(),
              annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout( margin=dict(l=0, r=10, t=28,b=0 ))
    fig.update_layout(
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ))
    # title='Histogram validations per travel route: {}'.format(route),
    
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig

def histogram_validations_zone(start_date,end_date,ZoneValue,a):
    resultados_demanda=models.histogram_validations_zone(start_date,end_date,ZoneValue,a)
    fig = px.histogram(resultados_demanda, x='cumsum_demanda', 
                       labels={'cumsum_demanda':'Número de validaciones por viaje'},width=510, height=400)
    fig.update_layout(xaxis_title_text = 'Number validations per ride', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(),
              annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout(margin=dict(l=0, r=10, t=35,b=0 ))
    fig.update_layout(title='Histogram validations per ride for all route, zone {}'.format(ZoneValue),
                                font=dict(
                                    family='Sherif',
                                    size=16,
                                    color = 'black',                                    
                                    ))
    
    
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig

###########################################################################################################
def heat_map_interactivition(start_date,end_date,ZoneValue,route,a):
    resultados=models.heatmap_interctive(start_date,end_date,ZoneValue,route,a)
    
    cat_type = CategoricalDtype(categories=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',z='cantidad_pasajeros',histfunc='sum',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Day name','hora':'Hour','count':'Total validations','cenefa':'bus stop'},
                            animation_frame='nombre_dia',
                            color_continuous_scale='reds',
                            category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y, height=400 ) 
    fig.update_layout(
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.update_yaxes(autorange= 'reversed',nticks=8)
    fig.update_xaxes(ticks='')
    # title='Validations per hour by bus stop {}'.format(route),
    # fig.layout.paper_bgcolor = '#073559'

    return fig

def heat_map_interactivition_zone(start_date,end_date,ZoneValue,a):
    resultados=models.heatmap_interctive_zone(start_date,end_date,ZoneValue,a)
    
    cat_type = CategoricalDtype(categories=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',z='cantidad_pasajeros',histfunc='sum',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Day name','hora':'Hour','count':'Total validations','cenefa':'bus stop'},
                            animation_frame='nombre_dia',
                            color_continuous_scale='reds',
                            category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y, height=400)
    fig.update_layout(
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    fig.update_yaxes(autorange= 'reversed',nticks=8)
    fig.update_xaxes(ticks='')
    # title='Validations per hour by bus stop {}'.format(ZoneValue),
    # fig.layout.paper_bgcolor = '#073559'

    return fig

##################################### BARRAS #########################################################

def average_number_buses_per_hour_zone(start_date,end_date,ZoneValue,a):
    df=models.average_number_buses_per_hour_zona(start_date,end_date,ZoneValue,a)
    fig = px.bar(df, x='hour', y='avg_num_bus', height=400 )
    
    fig.update_layout(title='Average quantity buses {} and {} for zone: {}'.format(start_date,end_date,ZoneValue),
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig

def average_number_buses_per_hour_route(start_date,end_date,ZoneValue,route,a):
    df=models.average_number_buses_per_hour_route(start_date,end_date,ZoneValue,route,a)
    fig = px.bar(df, x='hour', y='avg_num_bus', height=400 )
    
    fig.update_layout(
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
                    #   title='Average quantity buses {} and {} for route: {}'.format(start_date,end_date,route),
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig
#########################################################################################################
def average_number_buses_per_day_per_month_zone_all_routes(start_date,end_date,ZoneValue,a):
    df=models.average_number_buses_per_day_per_month_zona_all_routes(start_date,end_date,ZoneValue,a)
    fig = px.bar(df, x='commertial_route', y='avg_num_bus_per_day', height=400 )
    fig.update_layout(
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
                    #   title='Average quantity buses {} and {} for zone {}'.format(start_date,end_date,ZoneValue),
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig


def bar_total_valitations_zone_hour(start_date,end_date,ZoneValue,a):
    resultados=models.heatmap_interctive_zone(start_date,end_date,ZoneValue,a)
    result=resultados.drop(columns=['fecha_servicio','vehiculo_id','hora_validacion',
                                    'posicion','posicion_zero','cumsum_demanda','dia_semana'])
    result=result.groupby(['cenefa','hora','nombre_dia']).sum().reset_index()
    fig = px.bar(result, x="hora", y="cantidad_pasajeros", animation_frame="nombre_dia",
             hover_data=["cenefa"],
             labels={'nombre_dia':'Day name','hora':'Hour','cantidad_pasajeros':'Total validations','cenefa':'bus stop'},
             category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday']},
             width=510, height=400)
    
    fig.update_layout(title='Total validations  {} and {} for zone {}'.format(start_date,end_date,ZoneValue),
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    return fig

def bar_total_valitations_route_hour(start_date,end_date,ZoneValue,route,a):
    resultados=models.heatmap_interctive(start_date,end_date,ZoneValue,route,a)
    result=resultados.drop(columns=['fecha_servicio','vehiculo_id','hora_validacion',
                                    'posicion','posicion_zero','cumsum_demanda','dia_semana'])
    result=result.groupby(['cenefa','hora','nombre_dia']).sum().reset_index()
    fig = px.bar(result, x="hora", y="cantidad_pasajeros", animation_frame="nombre_dia",
             hover_data=["cenefa"],
             labels={'nombre_dia':'Day name','hora':'Hour','cantidad_pasajeros':'Total validations','cenefa':'bus stop'},
             category_orders={'nombre_dia':['monday','tuesday','wednesday','thursday','friday','saturday','sunday']},
             width=510, height=400)
    fig.update_layout(title='Total validations {} and {} for {}'.format(start_date,end_date, route),
                      font=dict(family='Sherif',size=16,color = 'black'),
                      margin=dict(l=0,r=0,t=35,b=0)                 
                      )
    # fig.layout.plot_bgcolor = '#84A4D5'
    # fig.layout.paper_bgcolor = '#073559'
    
    return fig