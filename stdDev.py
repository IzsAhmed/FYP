import pandas
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from urllib.request import urlopen
import json
import numpy as np
import csv


tableList = ["EconomicActivity.csv", "GainedQualifications.csv", "GeneralHealth.csv", "MaritalCivilStatus.csv", "Religion.csv"]
#tableList = ["EconomicActivity.csv"]
colSlct = "Qualification: Degree (for example BA, BSc), Higher degree (for example MA, PhD, PGCE); measures: Value"

def getColumnMean(df, column):
    return df[column].mean()

def getColumnStd(df, column):
    return df[column].std()


def detectOutliers(table, chosenCol):
    path = f"ProcessedData/{table}"
    thisTable = pd.read_csv(path)
    thisTable = thisTable[['geography', chosenCol]]
    print(getColumnMean(thisTable, chosenCol), getColumnStd(thisTable, chosenCol))

    thisTable['isOutlier'] = np.where((abs(thisTable[chosenCol] - getColumnMean(thisTable, chosenCol)) >= (getColumnStd(thisTable,chosenCol) * 2.5)) , True, False)
    print(thisTable.to_string())
    return thisTable



graph = detectOutliers(tableList[1], colSlct)

fig = px.scatter(graph, x="geography", y=colSlct, color='isOutlier')
fig.add_hline(y = getColumnMean(graph, colSlct), line_color="green", annotation_text="Median", annotation_position="bottom right")
fig.add_hline(y = getColumnMean(graph, colSlct) - (getColumnStd(graph, colSlct) * 2.5), line_color="red",  annotation_text="Lower Outlier Bound", annotation_position="bottom right")
fig.add_hline(y = getColumnMean(graph, colSlct) + (getColumnStd(graph, colSlct) * 2.5), line_color="red", annotation_text="Upper Outlier Bound",annotation_position="bottom right")
fig.show()
#dcc.Graph(figure=fig)