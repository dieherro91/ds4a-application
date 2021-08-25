# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Recall app
from app import app

#navegation_bar
Logout_buttom=dbc.Button('Logout',id='logout-button',color='danger',block=True,size='sm')

search_bar=dbc.Row(id='bar_nav_internal',
    children=[
    dbc.Col([dbc.Card(id='col_home',children=[dcc.Link('home', href='/home'),],),],align="center"),
    dbc.Col([dbc.Card(id='col_analysis',children=[dcc.Link('zones and route analysis', href='/analysis_data'),],),],align="center"),
    dbc.Col([dbc.Card(id='col_predictic',children=[dcc.Link('predictive model', href='/predictic_model'),],),], align="center"),
        dbc.Col([dbc.Card(id='col_team-83',children=[dcc.Link('team-83', href='/About_Us'),],),], align="center"),
    dbc.Col([dbc.Card(id='col_logout',children=[Logout_buttom,],),], align="center"),
    ])


navbar = dbc.Navbar(id='nav_bar',children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='https://www.masivocapital.co/images/ImagenesMC/LOGO-MASIVO-01.png', height="30px"),),
                    dbc.Col(dbc.NavbarBrand("Masivo Capital Data Analysis", className="title_nav_bar"),),
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

#tisdf=dbc.Container([dbc.Row([   ]),align="center",no_gutters=True,])
