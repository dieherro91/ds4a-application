import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from lib import title
from app import app
from data import initial_conditions

date_max=initial_conditions.max_date()
date_min=initial_conditions.min_date()

list_zones=initial_conditions.listZone()
list_aux_zone=[]



agd=dict()
for zone in list_zones:
    list_aux_zone.append(zone['label'])
wer={}
for zones in list_aux_zone:
  wer[zones]=initial_conditions.ruta_comercial(zones)


df_cluster=initial_conditions.data_frame_cluster()
####################################################################

DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("auto-transporte.jpg"), style={"width" : "700px" })],)

fluid_jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Div([
                html.H1("Masivo Capital", className="display-5"),
                html.P(
                    "Monitoreo del desempeño de operadores en la vía,"
                    "optimización de asignación de flota para movilización de  pasajeros.",
                    className="lead",
                ),
                DS4A_Img,
                ] ,className="text-center"),
                html.P(
                    "Gracias al analisis de la información proporcionada por el transmilenio a través   "
                    "de las operaciones diarias realizadas, podemos mejorar el servicio, disminuir costo de operación."
                    "Incremetar o maximizar la movilidad de pasajeros",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)
main_home_page= dbc.Container(
                id='container_home',
                children=[
                    dcc.Location(id='home-url',pathname='/home'),
                    title.navbar,
                    fluid_jumbotron
                         ]
)
                  