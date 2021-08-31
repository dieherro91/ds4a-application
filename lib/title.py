
#In this file are all the links for the navegation bar

import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from app import app

#logout buttom for the navegation bar
Logout_buttom=dbc.Button('Logout',id='logout-button',color='danger',block=True,size='sm')

#link for the pages in the navegation bar
search_bar=dbc.Row(id='bar_nav_internal',
    children=[
    dbc.Col([dbc.Card(id='col_home',children=[dcc.Link('Home', href='/home'),],),],align="center"),
    dbc.Col([dbc.Card(id='col_analysis',children=[dcc.Link('Analysis', href='/analysis_data'),],),],align="center"),
    dbc.Col([dbc.Card(id='col_predictic',children=[dcc.Link('Prediction', href='/predictic_model'),],),], align="center"),
    dbc.Col([dbc.Card(id='col_team-83',children=[dcc.Link('Team', href='/About_Us'),],),], align="center"),
    dbc.Col([dbc.Card(id='col_logout',children=[Logout_buttom,],),], align="center"),
            ],
                )

# navigation bar laylout
navbar = dbc.Navbar(id='nav_bar',children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"), height="70px"),),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://www.masivocapital.co",
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            search_bar, id="navbar-collapse", navbar=True, is_open=False
        ),
    ],
    color="dark",
    dark=True,
)