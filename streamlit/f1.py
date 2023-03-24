import streamlit as st
import fastf1.plotting
import pandas as pd
from fastf1 import plotting, utils
from results import qualification_results
from race import race_lap_telemetry
from stats import get_stats

fastf1.Cache.enable_cache('/tmp')  # replace with your cache directory

# enable some matplotlib patches for plotting timedelta values and load
# FastF1's default color scheme
fastf1.plotting.setup_mpl()

if __name__ == '__main__':
    st.set_page_config(page_title="F1 Analysis (by matusso)", layout="wide")

    selectedYear = st.sidebar.selectbox(
        "Choose year",
        (2019, 2020, 2021, 2022, 2023)
    )

    schedule = fastf1.get_event_schedule(selectedYear)
    locations = []
    for index, row in schedule.iterrows():
        if row["RoundNumber"] > 0:
            locations.append(row["Location"])

    with st.sidebar:
        circuitName = st.selectbox(
            "Choose a Circuit",
            (locations)
        )
        session = st.selectbox(
            "Choose a session",
            ('Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race')
        )

    st.header(str(selectedYear) + "/" + circuitName)
    tab1, tab2, tab3 = st.tabs(["Telemetry", "Stats", "Results"])

    with tab1:
        race_lap_telemetry(fastf1.get_session(selectedYear, circuitName, session))

    with tab2:
        get_stats(fastf1.get_session(selectedYear, circuitName, session))

    with tab3:
        qualification_results(fastf1.get_session(selectedYear, circuitName, 'Q'))
    
