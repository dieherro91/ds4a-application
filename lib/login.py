import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


login_users=html.Div([
    
    dcc.Location(id='login-url',pathname='/login',refresh=False),
    dbc.Container(
        children=[dbc.Row(
                    dbc.Col(
                        dbc.Card([
                             html.H4('Login',className='card-title', style={'color':'#ffff'}),
                             dbc.Input(id='login-email',placeholder='User-App'),
                             dbc.Input(id='login-password',placeholder='Assigned password',type='password'),
                             dbc.Button('Submit',id='login-button',color='primary',block=True),
                             html.Br(),
                             html.Div(id='login-alert'),
                             ],body=True
                                ), width=6
                            ),justify='center'
                         ),
                html.Br(),
                dbc.Row(
                     dbc.Col(
                         html.Img(src='https://css.mintic.gov.co/mt/mintic/new/img/logo-MinTIC.png',className="imagen_center",
                                  ),width=6,
                     ),justify='center',
                 ),
                html.Br(),
                dbc.Row(
                     dbc.Col(
                         html.Img(src="https://www.correlation-one.com/hubfs/c1logo_color.png",className="imagen_center",
                                  width="566px",height="50px",),width=6,
                     ), justify='center',
                     
                 ),
                 html.Br(),
                 dbc.Row(
                     dbc.Col(
                         html.Img(src='https://www.masivocapital.co/images/ImagenesMC/LOGO-MASIVO-01.png',className="imagen_center",
                                  width="287px",height="192px",),width=6, 
                     ),justify='center',
                 ),
                 ]#
            )
        ]
    )