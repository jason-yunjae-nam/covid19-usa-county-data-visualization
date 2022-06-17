from datetime import date
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import pycountry
import addfips

af = addfips.AddFIPS()

def loadData(fileName):
    data = pd.read_csv(fileName)
    data = data.drop(columns=['UID','iso2','iso3','code3','Province_State','Combined_Key','Country_Region','Lat','Long_'])
    data = data.groupby(['FIPS', 'Admin2']).agg('sum')
    return data

# def find_iso(name):
#     try:
#         return pycountry.countries.lookup(name).alpha_3
#     except:
#         return None

def find_fips(name):
    try:
        return str(int(name)).zfill(5)
    except:
        return None

def melt(df, date_list):
    return pd.melt(df, id_vars=['fips', 'county'], value_vars=date_list)

df = loadData('time_series_covid19_confirmed_US.csv')

df['fips_int'] = df.index.get_level_values('FIPS')
df['county'] = df.index.get_level_values('Admin2')
df['fips'] = df['fips_int'].apply(find_fips)
# df['iso_alpha_3'] = df['country'].apply(find_iso)

date_list = list(df.columns)

df = melt(df, date_list)

print(df)

map = px.choropleth(df,
                    fips='fips',
                    animation_frame='variable',
                    color='value',
                    hover_name='county',
                    color_continuous_scale='Reds',
                    range_color=[0, 2000],
                    scope='usa'
                    )

map.show()
map.write_html("example_map.html")