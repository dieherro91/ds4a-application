import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title
from app import app

DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("auto-transporte.jpg"), style={"width" : "700px" })],)

fluid_jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Div([
                html.H1("Team 83 - Cohort 5", className="display-5"),
                html.P(
                    "________________",
                    className="lead",
                ),
                DS4A_Img,
                ] ,className="text-center"),
                html.P(
                    "___________",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)
about_us_page= dbc.Container(
                
                id='container_home',
                children=[
                    dcc.Location(id='team_83_about-url',pathname='/About_Us'),
                    title.navbar,
                   
                    fluid_jumbotron
   
                         ]
)