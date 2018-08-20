# FinseDashboard
Dashboard for WSN Finse

Authors:
S. Filhol, Aug. 2018

License: see the License.txt file

See the data of the past month collected by our Wireless Sensor Network at the Finse Research Station. 


## Technical Overview
This dashboard is written using the Python library Dash. Data are updated every 6h

## TODO
- write a file to (pull_data.py):
    - create a local sqlite DB, or local file to store the data
    - pull latest data
    - delete data older than a month old
- adjust the rest of the app. Change curve color to red
- add a map to the index page, or an embedded google map 
- convert electrical conductivity plot to dots
- **add github capabilities to the server**
- **add a TOKEN key in the server bashrc, that the function in db_query.py can retreive**
- 

## Ressources:
- [GitHub - Acrotrend/awesome-dash: A curated list of awesome Dash (plotly) resources](https://github.com/Acrotrend/awesome-dash)
- [YouTube](https://www.youtube.com/watch?v=hRH01ZzT2NI)
- [🌟 Introducing Dash 🌟 – plotly – Medium](https://medium.com/@plotlygraphs/introducing-dash-5ecf7191b503)