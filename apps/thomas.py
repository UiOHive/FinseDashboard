import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app

import numpy as np
import db_query as db
import datetime

serial = 8596359061997376531


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


layout = html.Div(children=[
    html.Div([html.Link(href='/static/whitey.css', rel='stylesheet')]),
    dcc.Markdown('''
# Thomas Station

This station records information about air temperature, wind speed and direction, and snow depth. 

- Location: []()
- Sensors:
    - Decagon DS-2
    - Maxbotix
- Database ID: 8596359061997376531
- Available variables :
    - air temperature
    - wind speed
    - wind direction
    - Station battery
    - Station signal reception power (RSSI)

## Graph settings
### 1. Number of days since today to display
'''),
    dcc.Slider(id='ndays', min=2, max=32, step=2, value=14, marks={i: '{} days'.format(i) for i in range(2, 30, 2)}),
    dcc.Markdown(
'''
### 2. Temporal resolution to display
'''
    ),
    dcc.Slider(id='nintervals', min=0, max=3700, step=None, value=100,
               marks={5:'5s', 30:'30s', 60:'1min', 300:'5min', 600:'10min', 1800:'30min', 3600:'1h'}),

    html.Div(id='output_graphs_statflux'),
    dcc.Markdown('''
---
## Return to [Home](index)
''')
])


@app.callback(
    Output(component_id='output_graphs_statflux', component_property='children'),
    [Input(component_id='ndays', component_property='value'),
     Input(component_id='nintervals', component_property='value')]
)
def update_graph_table_flux(input_ndays, inter_sample):
    start = datetime.datetime.now() - datetime.timedelta(days=input_ndays)
    end = datetime.datetime.now()

    df_thomas = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=100000, interval=inter_sample)
    df_thomas_ws = df_thomas.loc[~np.isnan(df_thomas.ds2_speed)]
    df_thomas_ws = df_thomas_ws.reset_index()

    df_thomas_mb = df_thomas.loc[~np.isnan(df_thomas.mb_median)]
    df_thomas_mb = df_thomas_mb.reset_index()

    graph_content = html.Div([
        html.H2(children='Sonic Air Temperature'),
        dcc.Graph(
            id='gr1',
            figure={
                'data': [{
                    'x': df_thomas_ws.time,
                    'y': df_thomas_ws.ds2_temp, 'name': 'temp'}],
                'layout': {'yaxis': {'title': 'Temperature [degC]'}}
            }),
        html.H2(children='Wind speed'),
        dcc.Graph(
            id='gr2',
            figure={
                'data': [{
                    'x': df_thomas_ws.time,
                    'y': df_thomas_ws.ds2_speed, 'name': 'speed'}],
                'layout': {'yaxis': {'title': 'Wind speed [m/s]'}}
            }),
        html.H2(children='Wind direction'),
        dcc.Graph(
            id='gr3',
            figure={
                'data': [{
                    'x': df_thomas_ws.time,
                    'y': df_thomas_ws.ds2_dir, 'name': 'direction',
                    'mode': 'markers',
                    'marker': {'opacity': 0.5}}],

                'layout': {'yaxis': {'title': 'Wind direction [deg]'}}
            }),
        html.H2(children='Distance to snow'),
        dcc.Graph(
            id='gr4',
            figure={
                'data': [{
                    'x': df_thomas_mb.time,
                    'y': df_thomas_mb.mb_median/10, 'name': 'Distance'}],
                'layout': {'yaxis': {'title': 'Distance [cm]'}}
            }),
        html.H2(children='Battery level'),
        dcc.Graph(
            id='gr5',
            figure={
                'data': [{
                    'x': df_thomas.time.loc[~np.isnan(df_thomas.bat)],
                    'y': df_thomas.bat.loc[~np.isnan(df_thomas.bat)], 'name': 'Battery'}],
                'layout': {'yaxis': {'title': 'Battery level [%]'}}
            }),
        html.H2(children='Table head of Thomas station data'),
        generate_table(df_thomas.tail(100), 5)
    ])
    return graph_content



