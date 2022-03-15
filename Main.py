import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from urllib.request import urlopen
import json

with urlopen('https://opendata.arcgis.com/datasets/1782872283f648828142036f3b213fb3_0.geojson') as response:
    uk_districts = json.load(response)

pop_data = pd.read_csv("ons2data.csv")


pop_data.head()
uk_districts['features'][0]['properties']

fig = px.choropleth_mapbox(pop_data, locations="name", featureidkey="properties.LAD21NM", geojson=uk_districts, color="Median Age", hover_name="name", mapbox_style="carto-positron", zoom=4, center = {"lat": 55, "lon": 0})
fig.show()




#app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
#app.layout = html.Div([

#    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

#    html.Button('Submit', id='submit-val', n_clicks=0),

#    html.Div(id='output_container', children=[]),
#    html.Br(),

#    dcc.Graph(id='map', figure={})

#])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
#@app.callback(
#    [Output(component_id='map', component_property='figure')],
#    [Input(component_id='submit-val', component_property='n_clicks')]
#)
#def update_graph(button):

#    yes = button
    # Plotly Express
   # fig = px.choropleth_mapbox(pop_data, locations="name", featureidkey="properties.LAD21NM", geojson=uk_districts,
   #                            color="Median Age", hover_name="name", mapbox_style="carto-positron", zoom=4,
   #                            center={"lat": 55, "lon": 0})


#    return container, fig


# ------------------------------------------------------------------------------
#if __name__ == '__main__':
#    app.run_server(debug=True)