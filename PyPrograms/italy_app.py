import streamlit as st
import pandas as pd
import os

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

with st.sidebar:
    choice = st.radio("Navigation", ["About", "Slope", "Flag", "GRACE"])

@st.cache_data    
def collect_df():
    complete_df = pd.DataFrame()

    for file in os.listdir('C:\\Users\\Andrew\\Desktop\\gw_study\\girotto_lab\\processed_data\\all_combined'):
        df = pd.read_excel('C:\\Users\\Andrew\\Desktop\\gw_study\\girotto_lab\\processed_data\\all_combined\\' + file)
        complete_df = complete_df.append(df)
    return complete_df

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
    st.title("Location hue by flag")
    st.write("...")
    with open("map2.html", "r") as f:
        map_html = f.read()
        st.components.v1.html(map_html, width=700, height=500)

if choice == 'GRACE':
    st.title("Grace Data in Italy")
    st.write("...")
