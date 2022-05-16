import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from urllib.request import urlopen
import json

with urlopen('https://opendata.arcgis.com/datasets/1782872283f648828142036f3b213fb3_0.geojson') as response:
    uk_districts = json.load(response)

with open('tables.json') as json_file:
    tableList = json.load(json_file)

#pop_data = None
#pop_data = pd.read_csv("Data/Religion.csv")

app = Dash(__name__)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),


    dcc.Dropdown(id="slct_table",
                 options=tableList['Tables'],
                 multi=False,
                 value="EconomicActivity.csv",
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id="slct_data",
                 multi=False,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_data', component_property='value'),
     Input(component_id='slct_table', component_property='value')]
)
def update_graph(option_slctd, tableLoads):
    print(option_slctd)
    print(type(option_slctd))

    container = "The religion chosen by user was: {}".format(option_slctd)
    url = f"ProcessedData\{tableLoads}"
    pop_data = pd.read_csv(url)
    pop_data.head()

    # Plotly Express
    print(f"pop data is {pop_data}")
    fig = px.choropleth_mapbox(pop_data, locations="geography", featureidkey="properties.LAD21NM", geojson=uk_districts, color=option_slctd, hover_name="geography", mapbox_style="carto-positron", zoom=4, center = {"lat": 55, "lon": 0})

    return container, fig

@app.callback(
    [Output(component_id='slct_data', component_property='options'),
     Output(component_id='slct_data', component_property='value')],
    [Input(component_id='slct_table', component_property='value')]
)
def update_graph(option_slctd):

    columns = tableList[option_slctd]
    return columns, columns[0]['value']


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)