import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from urllib.request import urlopen
import json

#Setting up geojson file and config file
with urlopen('https://opendata.arcgis.com/datasets/1782872283f648828142036f3b213fb3_0.geojson') as response:
    uk_districts = json.load(response)
with open('tables.json') as json_file:
    tableList = json.load(json_file)

#Defines dash app
app = Dash(__name__)

#Methods for standard Deviation
def getColumnMean(df, column):
    return df[column].mean()

def getColumnStd(df, column):
    return df[column].std()


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Census Data Visualiser", style={'text-align': 'center'}),

    html.H3("Target Table and Column", style={'text-align': 'left'}),
    html.Div(
        className="row", children=[
            dcc.Dropdown(id="slct_table",
                         options=tableList['Tables'],
                         multi=False,
                         value="EconomicActivity.csv",
                         style={'width': "100%"}
                         ),

            dcc.Dropdown(id="slct_data",
                         multi=False,
                         style={'width': "100%"}
                         ),
    ], style=dict(display='flex')),

    html.H3("Secondary Table and Column", style={'text-align': 'left'}),
    html.Div(
        className="row", children=[
            dcc.Dropdown(id="slct_table2",
                         options=tableList['Tables'],
                         multi=False,
                         value="EconomicActivity.csv",
                         style={'width': "100%"}
                         ),

            dcc.Dropdown(id="slct_data2",
                         multi=False,
                         style={'width': "100%"}
                         ),

    ], style=dict(display='flex')),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={}, style={"border":"2px black solid"}),

    html.H3("Standard Deviation of all districts for selected Column", style={'text-align': 'center'}),
    dcc.Graph(id='columnStdDev', figure={}, style={"border":"2px black solid"}),
    html.H3("Outliers Above average", style={'text-align': 'left'}),
    html.Div(id='aboveAvg', children=[]),

    html.H3("Outliers Below average", style={'text-align': 'left'}),
    html.Div(id='belowAvg', children=[]),

    html.H3("Correlation and Trend Line between two selected Columns", style={'text-align': 'center'}),

    dcc.Graph(id='correlation', figure={}, style={"border":"2px black solid"})



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

    container = "The column chosen by user was: {}".format(option_slctd)
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

@app.callback(
    [Output(component_id='columnStdDev', component_property='figure'),
     Output(component_id='aboveAvg', component_property='children'),
     Output(component_id='belowAvg', component_property='children')],
    [Input(component_id='slct_data', component_property='value'),
     Input(component_id='slct_table', component_property='value')]
)
def detectOutliers(chosenCol, table):
    path = f"ProcessedData/{table}"
    thisTable = pd.read_csv(path)
    thisTable = thisTable[['geography', chosenCol]]
    print(getColumnMean(thisTable, chosenCol), getColumnStd(thisTable, chosenCol))

    thisMean = getColumnMean(thisTable, chosenCol)
    thisStd = getColumnStd(thisTable,chosenCol)

    thisTable['isOutlier'] = np.where((abs(thisTable[chosenCol] - thisMean) >= (thisStd * 2.5)) , True, False)
    print(thisTable.to_string())

    lowerBound = thisMean - (thisStd * 2.5)
    upperBound = thisMean + (thisStd * 2.5)

    fig = px.scatter(thisTable, x="geography", y=chosenCol, color='isOutlier')
    fig.add_hline(y = thisMean, line_color="green", annotation_text="Median", annotation_position="bottom right")
    fig.add_hline(y = lowerBound, line_color="red",  annotation_text="Lower Outlier Bound", annotation_position="bottom right")
    fig.add_hline(y = upperBound, line_color="red", annotation_text="Upper Outlier Bound",annotation_position="bottom right")

    abvOutlier = thisTable.loc[thisTable['isOutlier'] & (thisTable[chosenCol] >= upperBound)]['geography'].to_string()
    blwOutlier = thisTable.loc[thisTable['isOutlier'] & (thisTable[chosenCol] <= lowerBound)]['geography'].to_string()

    return fig, abvOutlier, blwOutlier

@app.callback(
    [Output(component_id='slct_data2', component_property='options'),
     Output(component_id='slct_data2', component_property='value')],
    [Input(component_id='slct_table2', component_property='value')]
)
def update_graph(option_slctd):

    columns = tableList[option_slctd]
    return columns, columns[0]['value']

@app.callback(
    Output(component_id='correlation', component_property='figure'),
    [Input(component_id='slct_table', component_property='value'),
     Input(component_id='slct_data', component_property='value'),
     Input(component_id='slct_table2', component_property='value'),
     Input(component_id='slct_data2', component_property='value')
     ]
)
def detectOutliers(table1, chosenCol1, table2, chosenCol2):
    path1 = f"ProcessedData/{table1}"
    thisTable1 = pd.read_csv(path1)
    thisTable1 = thisTable1[['geography', chosenCol1]]

    path2 = f"ProcessedData/{table2}"
    thisTable2 = pd.read_csv(path2)
    thisTable2 = thisTable2[['geography', chosenCol2]]

    merged = thisTable1.merge(thisTable2)
    correlate = merged.corr(method='pearson')
    print(merged.to_string())
    print(correlate)
    fig = px.scatter(merged, x=chosenCol1, y=chosenCol2, trendline="ols")
    return (fig)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)