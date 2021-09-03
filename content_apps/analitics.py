
#Analitic app is constructed in this file

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Recall app
from app import app
from lib import title, sidebar

###############################################################
#Module were the map plot validations is generate
map_validaciones_ubication_zone_route=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-1",type="default",
            children=[html.H4("Map Validations", className="card-title"), 
                      dcc.Graph(id='map_graph_route',),
                      ],
    ),),])

###############################################################
#Module were the scatter plot- validations and number of buses is generate
scatter_num_zonal=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-2",type="default",
            children=[html.H4("Validations vs Number of Buses Per Day Week",className="card-title"),
                      dcc.Graph(id='scatter_graph_zone',),
                      ],
    ),),])

###############################################################
#Module were the bar plot- avgerage num buses per route is generate
bar_average_number_buses_per_day_zone_all=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-3",type="default",
            children=[html.H4("Average Quantity Buses per Zone", className="card-title"),
                      dcc.Graph(id='average_number_buses_per_day_all_routes',),
                      ],
    ),),])

###############################################################
# Module were the heat map plot - total validations per hour per bus_stop is generate
heat_map_route=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-5",type="default",
            children=[html.H4("Validations Per Hour by Bus Stop", className="card-title"), 
                      dcc.Graph(id='heatmap_validation',),
                      ],
    ),),])

################################################################
#Similar to the heat but total validations are stacked in the bar plot is generate
bar_total_validations_hour=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-7",type="default",
            children=[html.H4("Total Validations Per Hour", className="card-title"),
                      dcc.Graph(id='bar_total_valitations',),
                      ],
    ),),])

################################################################
#Module were the bar plot with the average nand number of buses per hour is generate
bar_average_number_buses_per_hour=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-6",type="default",
            children=[html.H4("Average and Number Buses Per Hour", className="card-title"),
                      dcc.Graph(id='average_number_buses_per_hour',),
                      ],
    ),),])

###############################################################
#Module were the HISTOGRAM plot with the number of validations per travel route
histogram_validations_route=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-4",type="default",
            children=[html.H4("Histogram Validations Per Travel Route", className="card-title"),
                      dcc.Graph(id='histogram_validation',),
                      ],
    ),),])

#################################################################################
# Here the layout for the plots to use.
#################################################################################

analitics_stats = html.Div(
    [
        # Place the different graph components here.
        dbc.Row([
            dbc.Col([map_validaciones_ubication_zone_route],align="center", width="12", className='mt-1 mb-2 pl-1.5 pr-1.5')
        ], ),
        
       html.Br(), 
        
       dbc.Row([
            dbc.Col([scatter_num_zonal,],align="center",width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
            dbc.Col([bar_average_number_buses_per_day_zone_all,],align="center",width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),       
                ],),
        
        html.Br(),
        
        dbc.Row([
           dbc.Col([heat_map_route,],align="center", width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
           dbc.Col([bar_total_validations_hour],align="center", width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
               ] ), 
        dbc.Row([
            dbc.Col([bar_average_number_buses_per_hour],align="center",width="6"),
            dbc.Col([histogram_validations_route],align="center",width="6"),
           
               ] ), 
    ],
    className="ds4a-body",
)

#################################################################################
# Here the layout for the initial analitic page to use.
#################################################################################
DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("graphic_with_hand.jpg"), style={"width" : "420px" })],)
imagen_test= dbc.Jumbotron(id='jumboContainer',children=[
        dbc.Container(
            [
                html.Div([
                html.H2("Data Analysis", className="display-5 mt-2"),
                html.P(
                    "In this page you could visualized and analized, "
                    "validations and number of buses in two ways: ",
                    className="lead",
                ),
                DS4A_Img,
                html.H6(id='refrencia2', children=["https://www.lavozdelanzarote.com/uploads/s1/20/77/80/8/beneficio_1_766x440.jpeg"]),
                ] ,className="text-center"),
                html.P(
                    "                                "
                    "Route Analysis and Zone Analysis",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

#################################################################################
# Here the constructor for the analitic page were will change when the user press a btn
#################################################################################
analysis_page=html.Div(id='analysis_page_test',children=[dcc.Location(id='analysis-url',pathname='/analysis_data'),
                        dcc.ConfirmDialog(id='confirm', 
                                    message='Each analysis query takes a maximum of 30 seconds, if a plot is not display please click the analysis buttom again.',),
                        title.navbar,
                        sidebar.sidebar,
                        html.Div(id='replace_analysis',children=[imagen_test]),
                ],className="container-fluid bg-app",
)









