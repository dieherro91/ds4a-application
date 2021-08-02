from data import models
import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype

def make_graph_route_zonal(month_scatter,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_zonal(month_scatter,ZoneValue,RouteValue)
    fig=px.scatter(df, x="average_validations_per_bus", y="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week"],
                    title='Number of passangers vs number of buses ({})'.format(ZoneValue))
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=0))

    return fig

def make_graph_route_single(month,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_route(month,ZoneValue,RouteValue)
    fig=px.scatter(df, x="average_validations_per_bus", y="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week"],
                    title='Number of passangers vs number of buses ({})'.format(RouteValue))
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=0))

    return fig

def make_graph_route_single_hour(month,ZoneValue,RouteValue,hour):
    df=models.scatter_numPasajeros_numBuses_route_hour_weekday(month,ZoneValue,RouteValue,hour)
    fig=px.scatter(df, x="average_validations_per_bus", y="number_of_buses", color="commertial_route",
                    hover_data=["commertial_route","day_of_week"],
                    title='Number of passangers vs number of buses ({})'.format(RouteValue))
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=0))

    return fig




def graph1_validaciones_ubication_zone_route(month,ZoneValue,route):
    df=models.validaciones_ubication_zone_route(month,ZoneValue,route)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validations",hover_name="border",size="validations", zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    #
    return fig 



def histogram_validations(month,ZoneValue,route):
    resultados_demanda=models.histogram_validations(month,ZoneValue,route)
    fig = px.histogram(resultados_demanda, x='cumsum_demanda', labels={'cumsum_demanda':'Número de validaciones por viaje'},
                   title='Histogram number validations per travel {}'.format(route))
    fig.update_layout(xaxis_title_text = 'Número de validaciones por viaje', bargap = 0.1)
    fig.add_vline(x = resultados_demanda['cumsum_demanda'].mean(),
              annotation_text='promedio:{:.2f}'.format(resultados_demanda['cumsum_demanda'].mean()))
    fig.update_layout(autosize=True, margin=dict( autoexpand=True, l=100, r=60, t=110, ))
    
    return fig

def heat_map_interactivition(month,ZoneValue,route):
    resultados=models.heatmap_interctive(month,ZoneValue,route)
    
    cat_type = CategoricalDtype(categories=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'], ordered=True)
    resultados['nombre_dia'] = resultados['nombre_dia'].astype(cat_type)
    cat_type = CategoricalDtype(categories=[0,1,2,3,4,5,6], ordered=True)
    resultados['dia_semana'] = resultados['dia_semana'].astype(cat_type)

    #Getting the order of stops:
    order_cenefa = resultados[['posicion','cenefa']].sort_values(by='posicion').drop_duplicates()['cenefa']
    order_cenefa = list(order_cenefa)
    nbins_y = int(resultados['hora'].max() -  resultados['hora'].min())
    
    fig = px.density_heatmap(resultados, x='cenefa', y='hora',
                            hover_data = ['nombre_dia'],
                            labels={'nombre_dia':'Nombre Día','hora':'Hora','count':'Total de validaciones'},
                            animation_frame='nombre_dia',
                            category_orders={'nombre_dia':['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
                                              'cenefa': order_cenefa},
                            template='seaborn',
                            nbinsy = nbins_y)
    fig.update_layout(title='Validaciones por hora y por cenefa según el día',
                      autosize=True,
                      margin=dict(autoexpand=True, l=5, r=5, t=50,  )
                        )
    fig.update_yaxes(autorange= 'reversed',   nticks=24)

    return fig