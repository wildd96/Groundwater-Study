import streamlit as st
import pandas as pd
import os
#import ee

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

with st.sidebar:
    choice = st.radio("Navigation", ["About", "Slope", "Flag", "GRACE"])

def get_grace_data(latitude, longitude):
    point = ee.Geometry.Point(longitude, latitude)
    
    # Filter the GRACE dataset for the point location
    grace_data = grace_dataset.filterBounds(point)
    
    # Get the GRACE data for the point location as a time series
    grace_timeseries = ee.Image(grace_data.first()).reduceRegion(ee.Reducer.mean(), point, 5000).getInfo()
    
    # Convert the time series data to a pandas dataframe
    grace_df = pd.DataFrame(grace_timeseries.items(), columns=['date', 'mass_change'])
    grace_df['date'] = pd.to_datetime(grace_df['date'], unit='ms')
    
    return grace_df

@st.experimental_memo    
def collect_df():
    complete_df = pd.DataFrame()

    for file in os.listdir('C:\\Users\\Andrew\\Desktop\\gw_study\\girotto_lab\\processed_data\\all_combined'):
        df = pd.read_excel('C:\\Users\\Andrew\\Desktop\\gw_study\\girotto_lab\\processed_data\\all_combined\\' + file)
        complete_df = complete_df.append(df)
    return complete_df

@st.experimental_memo
def collect_flagged():
    flagged_table = pd.DataFrame()
    flagged_filepath = "C:\\Users\\Andrew\\Desktop\\gw_study\\girotto_lab\\processed_data\\all_matrix\\flagged-tables"

    for files in os.listdir(flagged_filepath):
        df = pd.read_excel(flagged_filepath + "\\" + files)
        df = df.iloc[[0], 1:].T
        flagged_table = flagged_table.append(df)
    flagged_table = flagged_table.reset_index()

flagged_df = collect_flagged()

complete_df = collect_df()

if choice == 'About':
    st.title("About")
    st.write("Welcome to page 1!")
    
if choice == 'Slope':
    option = st.selectbox("Choose a site for closer observation:", complete_df['codice'].unique())

    st.write("Your site:", option)
    
    st.title("Location hue by slope")
    st.write("...")
    with open("map.html", "r") as f:
        map_html = f.read()
        st.components.v1.html(map_html, width=700, height=500)

    df = complete_df[complete_df['codice'] == option]
    profile_report = df.profile_report()
    st_profile_report(profile_report)

if choice == 'Flag':
    flag_option = st.selectbox("Stats by flag: ", [2, 1, 0])

    st.title("Location hue by flag")
    st.write("...")
    with open("map2.html", "r") as f:
        map_html = f.read()
        st.components.v1.html(map_html, width=700, height=500)

    flag_df = complete_df[complete_df['codice'] == flag_option]
    profile_report = flag_df.profile_report()
    st_profile_report(profile_report)

if choice == 'GRACE':
    st.title("Grace Data in Italy")
    st.write("...")
