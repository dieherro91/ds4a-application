
#In his file are the functions for the auntentification in the login page.
##NOTE IMPORTANT all the functions in this file weren't made for team 83 
##NOTE this functions were extract from https://github.com/russellromney/basic-dash-auth-flow

from functools import wraps
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import session

# fake users dict   auth.py
users = {
    'DgoRomr':'adjsfbq5',
    'team83':'team-ds4a',
    'masivo-admin':'!hTW*r8Z0OEV',
}

def authenticate_user(credentials):
    '''
    generic authentication function
    returns True if user is correct and False otherwise
    '''
    #
    # replace with your code
    authed = (credentials['user'] in users) and (credentials['password'] == users[credentials['user']])
    # 
    #
    return authed

def validate_login_session(f):
    '''
    takes a layout function that returns layout objects
    checks if the user is logged in or not through the session. 
    If not, returns an error with link to the login page
    '''
    @wraps(f)
    def wrapper(*args,**kwargs):
        if session.get('authed',None)==True:
            return f(*args,**kwargs)
        return html.Div(
            dbc.Row(
                dbc.Col([dbc.Card([
                                html.H2('401 - Unauthorized',className='card-title'),
                                html.A(dcc.Link('Login',href='/login'))
                            ],body=True)
                    ],width=5
                ),justify='center'
            )
        )
    return wrapper