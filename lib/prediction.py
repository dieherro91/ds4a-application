import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title

prediction_page=html.Div([dcc.Location(id='prediciton-url',pathname='/predictic_model'),
            dbc.Container(id='container_prediction',
                children=[
                    title.navbar,
                    html.Br(),
                    html.Br(),
                    dbc.Row(dbc.Col([html.H2('Prediction page.')],),justify='center'),
                            html.Br(),
                            dbc.Row( []),
                            html.Br()
                         ],)
                  ])