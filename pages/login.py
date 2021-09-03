
#In this file are the layout for the login page.

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from app import app

#####################################################################################
# Login Layout
#####################################################################################
login_users=html.Div([    
    dcc.Location(id='login-url',pathname='/login',refresh=False),
    # view_login
    dbc.Container(
        children=[
            dbc.Row(
                     dbc.Col(
                         html.Img(src=app.get_asset_url("LOGO-MASIVO-01.png"),className="imagen_center",
                                  width="287px",height="192px",),width=6, 
                     ),justify='center',
                 ),
                 dbc.Row(
                    dbc.Col(
                        dbc.Card([
                             html.H4('Login',className='card-title muted text-center', style={'color':'black'}),
                             dbc.Input(id='login-email',placeholder='User-App',value=''),
                             dbc.Input(id='login-password',placeholder='Assigned password',type='password', value=''),
                             dbc.Button('Submit',id='login-button',color='primary',block=True),
                             html.Br(),
                             html.Div(id='login-alert'),
                             ],body=True
                                ), width=4
                            ),justify='center'
                         ),
                html.Br(),
                dbc.Row(
                     dbc.Col(
                         html.Img(src=app.get_asset_url("logo-MinTIC.png"),className="imagen_center",
                                  ),width=6,
                     ),justify='center',
                 ),
                 html.Br(),#
                dbc.Row(#
                     dbc.Col(
                          html.Img(src=app.get_asset_url("c1logo_color.webp"),className="imagen_center",
                                   width="566px",height="50px",),width=6,
                      ), justify='center',
                     
                  ),
                 html.Br(),
                 
                 ]
            )
        ], className="login"
    )