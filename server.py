#In his file are the functions for the server in the login page.
##NOTE IMPORTANT all the functions in this file weren't made for team 83 
##NOTE this functions were extract from https://github.com/russellromney/basic-dash-auth-flow

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True
app.title = 'Masivo Capital Data Analysis'

server = app.server
server.config['SECRET_KEY'] = 'k1LUZ1fZShowB6opoyUIEJkJvS8RBF6MMgmNcDGNmgGYr' # i know this should not be in version control...