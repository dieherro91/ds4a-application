import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from lib import title
from app import app

DS4A_Img = html.Div(children=[html.Img(src=app.get_asset_url("auto-transporte.jpg"), style={"width" : "700px" })],)
profiles = list()

profiles =  [["José Miguel Ferrario ", "Physicist", "jmferrariop@unal.edu.co", "Jose_Miguel.png","https://linkedin.com" ],
            ["Diego Hernando Romero Roa", "Chemical Engineer", "dihromeroro@unal.edu.co", "Diego_Romero.png", "https://linkedin.com"],
            ["Angel Alberto Castro Lancheros", "Physicist", "aa.castro10@uniandes.edu.co","angel_image.jpg", "https://linkedin.com"],
            ["Alejandra Perpiñán Barrios", "Petroleum Engineer", "maperpinanb@unal.edu.co","profile.png", "https://linkedin.com"],
            ["Julián Esteban Londoño", "Physics Engineer", "julondonor@unal.edu.co","profile.png", "https://www.linkedin.com/in/julondonor"],
            ["Jose Antonio Aviles Pacheco", "Systems Engineer", "joseavilesmnt@gmail.com", "profile.png", "https://www.linkedin.com/in/joseavilespacheco/"],
            ["Juan Pablo Gutiérrez Restrepo", "Computer Scientist", "jgutierrezre@unal.edu.co", "profile.png", "https://linkedin.com"]]

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

# p_1 = html.Div(children=output_profiles)
p_1 = dbc.Row(
    output_profiles
)

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
                p_1,
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