import pandas as pd
import streamlit as st
import geopandas as gpd
import plotly.figure_factory as ff
import plotly.express as px

st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")


df = pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", index_col=0)

st.header("1. Inspect the data 🔍")

st.write("`st.data_editor` allows us to display AND edit data")

st.data_editor(df)

st.header("2. Get started with a simple bar chart 📊")

st.write("Let's chart the US state population data from the year 2019")

st.bar_chart(df[['year', 'states', 'population']],
             x='states',
             y='population')


st.header("3. Now make it interactive 🪄")

st.write("It's your turn to select a year")

# Using st.selectbox
#selected_year = st.selectbox("Select a year",
#                             list(df.year.unique())[::-1])

# Using st.slider
selected_year = st.slider("Select a year", 2010, 2019)

# Using st.number_input
#selected_year = st.number_input("Enter a year",
#                                placeholder="Enter a year from 2010-2019",
#                                value=2019)

if selected_year:
    df_selected_year = df[df.year == selected_year]

    # Display chart
    st.bar_chart(df_selected_year,
                 x='states',
                 y='population')


import altair as alt 


st.header("Select a tab:")




tab1, tab2 = st.tabs(["Comparison of Population", "Map of the US"])
tab1.header("4. How about a line chart? 📈")

tab1.write("Track changes over time")


selected_state = tab1.multiselect('Select two states', options=df['states'].unique(), default=['New York', 'California'], max_selections=10)

#if selected_state:
#    df_selected_state = df[df.states == selected_state & df.states == selected_state2]

    # Display chart
#    tab1.bar_chart(df_selected_state,
#                 x='states',
#                 y='population')

df_line_chart = df[df['states'].isin(selected_state)]

c = (
    alt.Chart(df_line_chart)
     .mark_line()
     .encode(x=alt.X('year', axis=alt.Axis(format='d')),
             y=alt.Y('population'),
             color='states')
)

tab1.altair_chart(c, use_container_width=True)

### Tab 2

### Prepare the data
import json
from shapely.geometry import shape

# Convert the 'St Asgeojson' column to geometries
result = pd.read_csv('Test/us-population-2010-2019-reshaped.csv')
result['geometry'] = result['St Asgeojson'].apply(lambda x: shape(json.loads(x)))

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(result, geometry='geometry')

# Create a dictionary of GeoDataFrames
gdf_dict = {}
for i in gdf.year.unique():
    gdf_dict[f'{i}'] = gpd.GeoDataFrame(gdf.loc[gdf['year'] == i], geometry='geometry')

tab2.header("5. Interactive map 🗺️")
tab2.write("Please select a year to view the population by state on an interactive map")

# Using st.slider
selected_year2 = tab2.selectbox("Select a year",
                             list(gdf_dict.keys()))

if selected_year2:
    gdf_selected_year = gdf_dict[f'{selected_year2}']
    fig = px.choropleth(gdf_selected_year, geojson=gdf_selected_year.geometry, locations=gdf_selected_year.index, color='population', scope="usa", title=f'Population by State in {selected_year2}', hover_name='states')
    tab2.plotly_chart(fig)
