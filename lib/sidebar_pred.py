
#In this file are all the filtres and dropdowns that make the sidebar for the prediction page

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime

from pages import homes
import datetime


############################################################################# 
# Titles of the dropdows and filters for the side bar for the predictive page
#############################################################################
titleAnalysisType=html.Div(children=[html.H6('ANALYSIS TYPE SELECTION', id='titleAnalysisType_id_pre', className='item-selection',),],)
titleZone=html.Div(children=[html.H6('ZONE SELECTION', id='titleZone_id_pre', className='item-selection',),],)
titleRoute=html.Div(children=[html.H6('ROUTE SELECTION', id='titleRoute_id_pre', className='item-selection',),],)

title_date_range=html.Div(children=[html.H6('TRAINING DATE', id='title_month_pre', className='item-selection',),],)
title_date_range_pre=html.Div(children=[html.H6('PREDICTION DATE', id='title_month_pre_date', className='item-selection',),],)
title_date_exclutor=html.Div(children=[html.H6('DATE EXCLUDER', id='title_exlutor_pre', className='item-selection',),],)

#############################################################################
# Dropdowns layout
#############################################################################
drop_zone=html.Div(children=[dcc.Dropdown(id='zone_dropdown_pre',options=homes.list_zones,
                                        value='',
                                        style={'font-size':'12'},
                                        placeholder="Select a zone",
                                        ),
                            ],
                    )
drop_route=html.Div(children=[dcc.Dropdown(id='route_dropdown_pre',options=[],
                                           value='',style={'font-size':'12'},
                                           placeholder="Select a route",searchable=True,
                                           ),
                             ],
                    )

#############################################################################
# Date prediction layout
#############################################################################
date_prediction=html.Div(children=[
                            title_date_range_pre,
                            dcc.DatePickerSingle(
                                id='date_picker_predictor_pre',
                                calendar_orientation='horizontal',
                                initial_visible_month=homes.date_max,
                                min_date_allowed=homes.date_max + datetime.timedelta(days=1),
                                month_format='YYYY-MM-DD',
                                clearable=True,),
                                ],
                        )

#############################################################################
# CheckList
#############################################################################
ckecklist_strike=dcc.RadioItems(id='strike_day',options=[
                            {'label': 'Strike day', 'value': 'strike' },
                            {'label': 'Normal day', 'value': 'normal' },
                                                        ],
                            value='normal',
                            labelStyle={'display': 'inline-block'},
                            className='radio_buttom',
                            labelClassName="date-group-labels",
                            #labelCheckedClassName="date-group-labels-checked",
                                )  


#############################################################################
# Buttom that triggers the prediction layout
#############################################################################
bottoms_update=html.Div(children=[html.Button('Prediction Data', 
                                                id='btn_update_pre',
                                                n_clicks=0,
                                                style={'margin-left':'50px','margin-right': '50px'},
                                            ),
                                  ]
                        )

#############################################################################
# Sidebar prediction Layout
#############################################################################
sidebar = html.Div(
    [ 
        html.Hr(), 
        html.Div([titleZone, drop_zone,]),        
        html.Hr(),
        html.Div([titleRoute, drop_route,]),
        html.Hr(),
        date_prediction,
        ckecklist_strike,
        html.Hr(),
        html.Div([bottoms_update]),
        html.Hr(),
    ],
    className="ds4a-sidebar",
)