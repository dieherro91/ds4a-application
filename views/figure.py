from data import models
import pandas as pd
import plotly.express as px

def make_graph_route(month_scatter,ZoneValue,RouteValue):
    df=models.scatter_numPasajeros_numBuses_zonal(month_scatter,ZoneValue,RouteValue)
    fig=px.scatter(df, x="number_passengers_day", y="number_buses_day", color="comertial_route",
                    hover_data=["day","comertial_route","day_week"],
                    title='Number of passangers vs number of buses \n for zone {}'.format(ZoneValue),template="plotly_dark")
    fig.update_layout(margin=dict(l=5, r=5, t=50, b=0))

    return fig