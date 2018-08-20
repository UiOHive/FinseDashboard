'''
App to monitor WSN health

To be Done:
- redo plotting function to automatically plot a line for each station found in the query
- Split in two graph, one for lithium battery, and one for lead-acid (if relevant)
- make sure the color coding per waspmote is working

'''


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app

import db_query as db
import datetime
import pandas as pd

serial = {'middalselvi': 6951419298100303058,
          'thomas': 8596359061997376531,
          'marsh water table': 3390197892757083161}


layout = html.Div(children=[
    html.Div([html.Link(href='/static/whitey.css', rel='stylesheet')]),
    dcc.Markdown('''
# Network Health

App to monitor health of the wireless network. It keeps track of units battery level, signal quality (RSSI), and latest commit of data to the Meshpi     


## Graph settings
### 1. Number of days since today to display
'''),
    dcc.Slider(id='ndays', min=0, max=300, step=10, value=15, marks={i: '{} days'.format(i) for i in range(5, 290, 5)}),
    html.Div(id='output_graphs_health'),
    dcc.Markdown('''
---
## Return to [Home](index)
''')
])


@app.callback(
    Output(component_id='output_graphs_health', component_property='children'),
    [Input(component_id='ndays', component_property='value')]
)
def update_graph_table_flux(input_ndays):

    df = get_data(input_ndays)

    df_rssi = df.dropna(subset=['rssi'])

    graph_content = html.Div([
        html.H2(children='Battery level'),
        dcc.Graph(
            id='gr1',
            figure={
                'data': [
                    {
                        'x': df.time.loc[df.serial == df.serial[0]],
                        'y': df.bat.loc[df.serial == df.serial[0]],
                        'name': df.serial[0]
                    },
                    {
                        'x': df.time.loc[df.serial == df.serial[1]],
                        'y': df.bat.loc[df.serial == df.serial[1]],
                        'name': df.serial[1]
                    },
                    {
                        'x': df.time.loc[df.serial == df.serial[2]],
                        'y': df.bat.loc[df.serial == df.serial[2]],
                        'name': df.serial[2]
                    }],
                'layout': {'yaxis': {'title': 'Battery level [%]'}}
            }),
        html.H2(children='RSSI'),
        dcc.Graph(
            id='gr2',
            figure={
                'data': [
                    {
                        'x': df_rssi.time.loc[df_rssi.serial == df_rssi.serial[0]],
                        'y': df_rssi.rssi.loc[df_rssi.serial == df_rssi.serial[0]],
                        'name': df_rssi.serial[0],
                        'mode': 'markers'
                    },
                    {
                        'x': df_rssi.time.loc[df_rssi.serial == df_rssi.serial[1]],
                        'y': df_rssi.rssi.loc[df_rssi.serial == df_rssi.serial[1]],
                        'name': df_rssi.serial[1],
                        'mode': 'markers'
                    },
                    {
                        'x': df_rssi.time.loc[df_rssi.serial == df_rssi.serial[2]],
                        'y': df_rssi.rssi.loc[df_rssi.serial == df_rssi.serial[2]],
                        'name': df_rssi.serial[2],
                        'mode': 'markers'
                    }],
                'layout': {'yaxis': {'title': 'RSSI [dB]'}}
            })
    ])
    return graph_content


def get_data(input_ndays):
    start = datetime.datetime.now() - datetime.timedelta(days=input_ndays)
    end = datetime.datetime.now()

    df = db.query_df(fields=['bat', 'rssi'], tags=['serial'], time__gte=start, time__lte=end,
                     limit=100000)
    df.set_index(pd.to_datetime(df.time), inplace=True)
    return df
