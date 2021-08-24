import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title

# main_home_page=html.Div([dcc.Location(id='home-url',pathname='/home'),
#             dbc.Container(id='container_home',
#                 children=[
#                     title.navbar,
#                     html.Br(),
#                     html.Br(),
#                     dbc.Row(dbc.Col([html.H2('Home page.')],),justify='center'),
#                             html.Br(),
#                             dbc.Row( []),
#                             html.Br()
#                          ],)
#                   ])

main_home_page= dbc.Container(
                
                id='container_home',
                children=[
                    dcc.Location(id='home-url',pathname='/home'),
                    title.navbar,
                    html.Br(),
                    html.Br(),
                    dbc.Row(dbc.Col([html.H2('Home page.')],),justify='center'),
                            html.Br(),
                            dbc.Row( []),
                            html.Br()
                         ],)
                  