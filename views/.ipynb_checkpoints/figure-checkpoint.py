from data import models
import pandas as pd
import plotly.express as px

def make_graph_route(month_scatter,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_zonal(month_scatter,ZoneValue,RouteValue)
    fig=px.scatter(df, x="number_passengers_day", y="number_buses_day", color="comertial_route",
                    hover_data=["day","comertial_route","day_week"],
                    title='Number of passangers vs number of buses \n for zone {}'.format(ZoneValue))
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=0))

    return fig




def graph1_validaciones_ubication_zone_route(month,ZoneValue,route):
    df=models.validaciones_ubication_zone_route(month,ZoneValue,route)
    fig = px.scatter_mapbox(df ,lat='latitud', lon='longitud',color="validations",hover_name="border",size="validations", zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    #
    return fig 


