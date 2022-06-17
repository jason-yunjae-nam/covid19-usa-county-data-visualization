import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

baseURL = "https://resources-covid19canada.hub.arcgis.com/datasets/covid19canada::provincial-daily-totals/explore"

def loadData (fileName, columnName):
    data = pd.read_csv(baseURL + fileName)
    #.drop(['Lat', 'Long'], axis=1).melt(id_vars=['Province/State', 'Country/Region'], var_name='date', value_name=columnName).astype({'date':'datetime64[ns]', columnName:'Int64'}, errors='ignore')
    data['Province/State'].fillna('<all>', inplace=True)
    data[columnName].fillna(0, inplace=True)
    return data

print(loadData("data.csv", "Province"))