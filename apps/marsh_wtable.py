import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app

import numpy as np
import db_query as db
import datetime

serial = 3390197892757083161


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
# Marsh Water Table Station

Located in the marshland at Finse, this sensor provides the height of the water table in the valley

- Location: 
- Sensor: [Decagon ctd-10](https://www.metergroup.com/environment/products/hydros-21-water-level-monitoring/)
- Database ID: 3390197892757083161
- Available variables :
    - water depth
    - water temperature
    - water electrical conductivity
    - Station battery
    - Station signal reception power (RSSI)

## Graph settings
### 1. Number of days since today to display
''' ),
    dcc.Slider(id='ndays', min=0, max=370, step=10, value=14,marks={i: '{} days'.format(i) for i in range(0,360,10)}),
    dcc.Markdown(
'''
### 2. Temporal resolution to display
'''
    ),
    dcc.Slider(id='nintervals', min=0, max=3600*10, step=None, value=100,
               marks={600:'10min', 1800:'30min', 3600:'1h', 7200:'2h', 18000:'5h'}),

    html.Div(id='output_graphs_marsh'),
    dcc.Markdown('''
## Page future development:
- See to show water level in a abstracted cross section

- get shared x-axis for the three plots
- have an input box setting the start and final date to display, default being 15 days until now

---
## Return to [Home](index)

''')
])



@app.callback(
    Output(component_id='output_graphs_marsh', component_property='children'),
    [Input(component_id='ndays', component_property='value'),
     Input(component_id='nintervals', component_property='value')]
)
def update_graph_table(input_ndays, inter_samples):
    start = datetime.datetime.now() - datetime.timedelta(days=input_ndays)
    end = datetime.datetime.now()


    df_middal = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=100000, interval=inter_samples)
    df = df_middal.loc[~np.isnan(df_middal.ctd_depth)]
    df = df.reset_index()
    df.ctd_cond.loc[df.ctd_cond < 0.01] = np.nan

    graph_content = html.Div([
        html.H2(children='Water Discharge'),
        dcc.Graph(
            id='gr1',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_depth / 10, 'name': 'depth'}],
                'layout': {'yaxis': {'title': 'Water Depth [cm]'}}
            }),
        html.H2(children='Water Temperature'),
        dcc.Graph(
            id='gr2',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_temp, 'name': 'temp'}],
                'layout': {'yaxis': {'title': 'Temperature [degC]'}}
            }),
        html.H2(children='Water Electrical Conductivity'),
        dcc.Graph(
            id='gr3',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_cond, 'name': 'cond'}],
                'layout': {'yaxis': {'title': 'Electrical conductivity [dS/m]'}}
            }),
        html.H2(children='Table head of Marsh water table'),
        generate_table(df.tail(100), 5)]
    )
    return graph_content

