import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title

about_us_page=html.Div([dcc.Location(id='team_83_about-url',pathname='/About_Us'),
            dbc.Container(id='container_home',
                children=[
                    title.navbar,
                    html.Br(),
                    html.Br(),
                    dbc.Row(dbc.Col([html.H2('about us page.')],),justify='center'),
                            html.Br(),
                            dbc.Row( []),
                            html.Br()
                         ],)
                  ])