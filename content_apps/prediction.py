
#Prediction app is constructed in this file

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

from lib import title, sidebar_pred
from app import app


#######################################################################################
#Module were the Cluster plot is build  
clustering_predictor=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-8",type="default",
            children=[html.H4("Clustering Routes", className="card-title"), 
                      dcc.Graph(id='clustering',),
                      dbc.Label("Cluster count"),
                      dbc.Input(id='cluster-count', type="number", value=6),
                      ],
    ),),])

#######################################################################################
#Module were the table with the Cluster plot is build  
table_cluster=dbc.Card([dbc.CardBody(dcc.Loading(
            id="loading-8",
            type="default",
            children=[html.H4("Similar Clustering Routes", className="card-title"), 
                dash_table.DataTable(id='table_cluster',
                    columns=[{"name":'route', "id": 'route'},
                            {"name": 'num bus stops', "id": 'num_bus_stops'},
                            {"name": 'num passengers', "id": 'num_validations'},
                            {"name": 'cluster', "id": 'cluster'},
                            {"name": 'length bus route', "id": 'length_bus_route'},
                            ],
                    style_header={'backgroundColor': 'rgb(43, 139, 206)'},
                    style_cell={'textAlign': 'center',
                                'color': 'black'},
                    style_cell_conditional=[
                            {
                                'if': {'column_id': 'length_bus_route'},
                                'textAlign': 'right'
                            }],
                )
                    ],
        ),),],)

map_prediction=dbc.Card([dbc.CardBody(dcc.Loading(id="loading-9",type="default",
            children=[html.H4("Prediction Passengers", className="card-title"),
                    dcc.RadioItems(id='selection_graph',
                    options=[{'label': 'Map street  ', 'value': 'Map_street'},
                            {'label': '  Bar hours', 'value': 'Bar_hours'}
                            ],
                    value='Map_street',
                    labelStyle={'display': 'block'},
                    style={'font-size':'20px'},
                    className='radio_buttom',
                    labelClassName="date-group-labels",
                    #labelCheckedClassName="date-group-labels-checked",
                    ),
                      dcc.Graph(id='map_graph_prediction_route',),
                      ],
    ),),])

#################################################################################
# Here the layout for the plots to use.
#################################################################################
prediction= html.Div(
    [
        # Place the different graph components here.
        
        dbc.Row([
            dbc.Col([clustering_predictor],align="center",width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
            dbc.Col([table_cluster],align="center",width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),       
                ],),
        
        html.Br(),
        
        dbc.Row([
            dbc.Col([map_prediction], width="12", className='mt-1 mb-2 pl-1.5 pr-1.5')
        ], ),#map_prediction
        
       html.Br(), 
     
       
        
        dbc.Row([
            dbc.Col([],width="6"),
            dbc.Col([],width="6"),
               ] ), 
    ],
    className="ds4a-body",
)


#################################################################################
# Here the layout for the initial predictive page to use.
#################################################################################
DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("predicticve_img.png"), style={"width" : "420px" })],)
imagen_test= dbc.Jumbotron(id='jumboContainer_predict',children=[
        dbc.Container(
            [
                html.Div([
                html.H2("Predictive Analysis", className="display-5"),
                html.P(
                    "In this page you could visualized and predict"
                    "validations with",
                    className="lead",
                ),
                DS4A_Img,
                html.H6(id='refrencia1', children=["https://www.ehcos.com/wp-content/uploads/2017/03/What-Doctors-and-Nurses-Expect-of-Big-Data-Predictive-Analytics-in-the-ICU.png"]),
                ] ,className="text-center"), 
                html.P(
                    "Random Forest",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

#################################################################################
# Here the constructor for tha predictive page were will change when the user press a btn
#################################################################################
prediction_page=html.Div([dcc.Location(id='prediciton-url',pathname='/predictic_model'),
                        title.navbar,
                        sidebar_pred.sidebar,
                        html.Div(id='replace_analysis_prediction',children=[imagen_test]),
                ],className="container-fluid bg-app",
)
