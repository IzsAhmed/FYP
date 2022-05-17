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

col1Slct = "Economic Activity: Economically active: Employee: Full-time; measures: Value"
col2Slct = "Qualification: Degree (for example BA, BSc), Higher degree (for example MA, PhD, PGCE); measures: Value"

tableSlct1 = tableList[0]
tableSlct2 = tableList[1]


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
    return (merged, correlate)

correlation = detectOutliers(tableSlct1, col1Slct, tableSlct2, col2Slct)


fig = px.scatter(correlation[0], x=col1Slct, y=col2Slct, trendline="ols")
fig.show()

'''
graph = detectOutliers(tableList[1], colSlct)

fig = px.scatter(graph, x="geography", y=colSlct, color='isOutlier')
fig.add_hline(y = getColumnMean(graph, colSlct), line_color="green", annotation_text="Median", annotation_position="bottom right")
fig.add_hline(y = getColumnMean(graph, colSlct) - (getColumnStd(graph, colSlct) * 2.5), line_color="red",  annotation_text="Lower Outlier Bound", annotation_position="bottom right")
fig.add_hline(y = getColumnMean(graph, colSlct) + (getColumnStd(graph, colSlct) * 2.5), line_color="red", annotation_text="Upper Outlier Bound",annotation_position="bottom right")
fig.show()'''