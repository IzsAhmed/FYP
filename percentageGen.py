import pandas
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from urllib.request import urlopen
import json

import numpy as np
import csv

def percentage(part, whole):
  perc =  100 * float(part)/float(whole)
  return round(perc, 2)

tableList = ["EconomicActivity.csv", "GainedQualifications.csv", "GeneralHealth.csv", "MaritalCivilStatus.csv", "Religion.csv"]

for table in tableList:
    path = f"Data/{table}"

    csvData = list(csv.reader(open(path)))
    for j in range(1, len(csvData), 1):
        row = csvData[j]
        #print(row)
        for i in range(5, len(row), 1):
            row[i] = percentage(row[i], row[4])
        #print(row)

    processPath = f"ProcessedData/{table}"
    with open(processPath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csvData)

