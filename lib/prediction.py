import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title, sidebar_predict
from app import app

prediction= html.Div(
    [
        # Place the different graph components here.
       
        dbc.Row([
            dbc.Col([html.H2('Prediction page.')], width="12", className='mt-1 mb-2 pl-1.5 pr-1.5')
        ], ),
        
       html.Br(), 
        
       dbc.Row([
            
            dbc.Col([],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
            dbc.Col([],width="6", className='mt-1 mb-2 pl-1.5 pr-1.5'),
                        
                ],),
        
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


imagen_test=html.Div(id='imagen_tested_prediction',children=[
                        html.Div(children=[html.Img(src=app.get_asset_url("auto-transporte.jpg"), style={"width" : "700px" })],),
                        html.H1("Zona para la primera pagina del predictic model pagina descriptiva",id='text_warning'),
                ],className="container-fluid bg-app",
)


alert_no_dropdows=html.Div([html.Br(),
             html.Br(),
             html.H1("Please Complete the options in the side bar")],className="container-fluid bg-app",) 





prediction_page=html.Div([dcc.Location(id='prediciton-url',pathname='/predictic_model'),
                        title.navbar,
                        sidebar_predict.sidebar,
                        html.Div(id='replace_analysis_prediction',children=[imagen_test]),
                ],className="container-fluid bg-app",
)
