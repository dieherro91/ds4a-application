
#In this file are the layout for the team-83 (About us) page

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title
from app import app

############################# profiles of the members of the team 83#####################################
profiles = list()
profiles =  [
            ["Jose Antonio Aviles Pacheco", "Systems Engineer", "joseavilesmnt@gmail.com", "Aviles.png", "https://www.linkedin.com/in/joseavilespacheco/"],
            ["Angel Alberto Castro Lancheros", "Physicist", "aa.castro10@uniandes.edu.co","angel_image.jpg", "https://www.linkedin.com/in/angel-alberto-castro-lancheros-42358726/"],
            ["José Miguel Ferrario ", "Physicist", "jmferrariop@unal.edu.co", "Jose_Miguel.png","https://www.linkedin.com/in/jmferrariop/" ],
            ["Juan Pablo Gutiérrez Restrepo", "Computer Scientist", "jgutierrezre@unal.edu.co", "Juan.png", "https://www.linkedin.com/in/jgutierrezre/"],
            ["Julián Esteban Londoño", "Physics Engineer", "julondonor@unal.edu.co","Julian.png", "https://www.linkedin.com/in/julondonor"],
            ["Alejandra Perpiñán Barrios", "Petroleum Engineer", "maperpinanb@unal.edu.co","Alejandra.png", "https://www.linkedin.com/in/maria-perpi%C3%B1an-barrios/"],
            ["Diego Hernando Romero Roa", "Chemical Engineer", "dihromeroro@unal.edu.co", "Diego_Romero.png", "https://www.linkedin.com/in/diego-hernando-romero-roa-6744b7195/"],
        
            ]

output_profiles = []
for profile in profiles:
    output_profiles.append(dbc.Col(dbc.Card(
        [
            html.Div([dbc.CardImg(src="assets/profiles/"+profile[3], top=True)], className="overflow-hidden w-100 item-image"),
            dbc.CardBody(
                [
                    html.H5(profile[0], className="card-title"),
                    html.P(
                            profile[1],
                            className="card-text",
                            ),
                    dbc.Button("Linkedin", color="primary", href=profile[4]),
                ]
                        ),
        ],
        style={"width": "14rem"},
     ), className="back-card mb-4", width=3
    )
   )
p_1 = dbc.Row(output_profiles)

#####################################################################################
# Team 83 Layout
#####################################################################################
fluid_jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Div([
                html.H1("Team 83 - Cohort 5", className="display-5 mt-2"),
                # html.P("________________",
                #        className="lead",),
                p_1,
                ] ,className="text-center"),
                # html.P("___________",
                #     className="lead",
                # ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

#################################################################################
# Here the constructor for the home page with the about us page 
#################################################################################
about_us_page= dbc.Container(
                id='container_home',
                children=[dcc.Location(id='team_83_about-url',pathname='/About_Us'),
                          title.navbar, 
                          fluid_jumbotron
                          ]
                            )