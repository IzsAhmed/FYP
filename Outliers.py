import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from urllib.request import urlopen
import json
import numpy as np
import csv



def getColumnMean(df, column):
    return df[column].mean()

def getColumnStd(df, column):
    return df[column].std()

def detectOutliers(table, chosenCol):
    path = f"ProcessedData/{table}"
    thisTable = pd.read_csv(path)
    thisTable = thisTable[['geography', chosenCol]]
    print(getColumnMean(thisTable, chosenCol), getColumnStd(thisTable, chosenCol))

    thisMean = getColumnMean(thisTable, chosenCol)
    thisStd = getColumnStd(thisTable,chosenCol)

    thisTable['isOutlier'] = np.where((abs(thisTable[chosenCol] - thisMean) >= (thisStd * 2.5)) , True, False)
    print(thisTable.to_string())

    fig = px.scatter(graph, x="geography", y=chosenCol, color='isOutlier')
    fig.add_hline(y = thisMean, line_color="green", annotation_text="Median", annotation_position="bottom right")
    fig.add_hline(y = thisMean - (thisStd * 2.5), line_color="red",  annotation_text="Lower Outlier Bound", annotation_position="bottom right")
    fig.add_hline(y = thisMean - (thisStd * 2.5), line_color="red", annotation_text="Upper Outlier Bound",annotation_position="bottom right")
    return fig
