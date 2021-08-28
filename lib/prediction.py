import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title, sidebar_pred
from app import app

clustering_predictor=dbc.Card([dbc.CardBody(dcc.Loading(
            id="loading-8",
            type="default",
            children=[html.H4("Clustering Routes", className="card-title"), 
                      dcc.Graph(id='clustering',),
                      dbc.Label("Cluster count"),
                      dbc.Input(id='cluster-count', type="number", value=5),],),),])


prediction= html.Div(
    [
        # Place the different graph components here.
        dbc.Row([
            
            dbc.Col([clustering_predictor],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
            dbc.Col([],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
                        
                ],),
        
        html.Br(),
        
        dbc.Row([
            dbc.Col([], width="12", className='mt-1 mb-2 pl-1.5 pr-1.5')
        ], ),
        
       html.Br(), 
        
       
        
       dbc.Row([
           dbc.Col([], width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
           dbc.Col([], width="6",className='mt-1 mb-2 pl-1.5 pr-1.5'),
       
               ] ), 
        
        dbc.Row([
            dbc.Col([],width="6"),
            dbc.Col([],width="6"),
           
               ] ), 

    ],
    className="ds4a-body",
)



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
                ] ,className="text-center"),
                html.P(
                    "XGBoost Regressor",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

prediction_page=html.Div([dcc.Location(id='prediciton-url',pathname='/predictic_model'),
                        title.navbar,
                        sidebar_pred.sidebar,
                        html.Div(id='replace_analysis_prediction',children=[imagen_test]),
                ],className="container-fluid bg-app",
)
