import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import middals, thomas, marsh_wtable, flux_stationnary, wsn_health


app.layout = html.Div([
    html.Div([html.Link(href='/static/whitey.css', rel='stylesheet')]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/middals':
         return middals.layout
    elif pathname == '/apps/thomas':
         return thomas.layout
    elif pathname == '/apps/marsh_wtable':
        return marsh_wtable.layout
    elif pathname == '/apps/flux_stationnary':
         return flux_stationnary.layout
    elif pathname == '/apps/wsn_health':
        return wsn_health.layout
    else:
        return(home_page_content())


def home_page_content():
    return(html.Div([
        html.Div([html.Link(href='/static/whitey.css', rel='stylesheet')]),
        dcc.Markdown(''' 
# Finse Sensor Network
List of stations providing live data from Finse

## Eddy-Covariance Stations
- [Stationary flux](/apps/flux_stationnary) weather station
- Mobile Flux station (TO BE ADDED)

## Wireless Sensor Network

- [Middalselvi discharge station](/apps/middals)
- [Thomas station](/apps/thomas)
- [Marsh water table](/apps/marsh_wtable)
- [Network health](/apps/wsn_health)
''')

    ]))





if __name__ == '__main__':
   app.run_server(debug=True)
#    app.run_server(port=8000, host='158.39.75.185')
