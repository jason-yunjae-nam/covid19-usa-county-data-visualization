from datetime import date
import plotly.express as px
import pandas as pd
import json

# load geo json data
with open('geojson-counties-fips.json') as response:
    counties = json.load(response)

# load us county covid confirmed cases csv data
def loadData(dataURL):
    df = pd.read_csv(dataURL)
    df = df.drop(columns=['UID','iso2','iso3','code3','Province_State','Combined_Key','Country_Region','Lat','Long_'])
    df = df.groupby(['FIPS', 'Admin2']).agg('sum')
    return df

# format county fips
def find_fips(name):
    try:
        return str(int(name)).zfill(5)
    except:
        return None

df = loadData('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

date_list1 = list(df.columns)
date_list = date_list1[::len(date_list1)//24] # selection of dates

df['fips'] = df.index.get_level_values('FIPS') # copy fips index values to new column 'fips'
df['county'] = df.index.get_level_values('Admin2') # copy county name index calues to new column 'county'
df['fips'] = df['fips'].apply(find_fips)

df = pd.melt(df, id_vars=['fips','county'], value_vars=date_list, var_name='date', value_name='cases') # unpivot dataframe from wide format to long format

# generate choropleth map
map = px.choropleth(df,
                    geojson=counties,
                    locations='fips',
                    animation_frame='date',
                    color='cases',
                    hover_name='county',
                    color_continuous_scale='Reds',
                    range_color=[0, 22000],
                    scope='usa'
                    )
map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# improve legend
map.update_layout(coloraxis_colorbar=dict(
    thicknessmode="pixels", thickness=10,
    lenmode="pixels", len=400,
    yanchor="top", y=0.8,
    ticks="outside", ticksuffix=" ",
    dtick=5000
))

map.show()
map.write_html("covid19-us-counties-interactive-data.html")
