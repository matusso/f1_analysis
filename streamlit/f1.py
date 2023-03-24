import streamlit as st
import numpy as np
import time
import pandas as pd

import matplotlib.pyplot as plt
import fastf1.plotting
from fastf1 import plotting
from fastf1 import utils

#fastf1.Cache.enable_cache('./cache')  # replace with your cache directory

# enable some matplotlib patches for plotting timedelta values and load
# FastF1's default color scheme
fastf1.plotting.setup_mpl()


@st.cache_data
def load_q(session, telX, telY, lblX, lblY, dD, dO, dT):
    driver_dict = dD
    driverOne = dO
    driverTwo = dT

    ver_lap = session.laps.pick_driver(driver_dict[driverOne][0]).pick_fastest()
    ham_lap = session.laps.pick_driver(driver_dict[driverTwo][0]).pick_fastest()

    ver_tel = ver_lap.get_car_data().add_distance()
    ham_tel = ham_lap.get_car_data().add_distance()

    fig, ax = plt.subplots()
    ax.plot(ver_tel[telX], ver_tel[telY], color='#'+driver_dict[driverOne][1], label=driver_dict[driverOne][0])
    ax.plot(ham_tel[telX], ham_tel[telY], color='#'+driver_dict[driverTwo][1], label=driver_dict[driverTwo][0])

    #ax.set_xlabel('Distance in m')
    #ax.set_ylabel('Speed in km/h')
    ax.set_xlabel(lblX)
    ax.set_ylabel(lblY)

    return fig
    

def draw_chart(session):
    session.load()
    driver_dict = {}

    for d in session.drivers:
        driver = session.get_driver(d)
        driver_dict[driver['FullName']] = [driver['Abbreviation'], driver['TeamColor']]

    col1, col2 = st.columns(2)
    with col1:
        driverOne = st.selectbox('Select driver #1', driver_dict.keys())
    
    with col2:
        driverTwo = st.selectbox('Select driver #2', driver_dict.keys())

    col1, col2 = st.columns(2)
    with col1:
        st.header("Gear")
        fig = load_q(session, telX="Distance", telY="nGear", lblX="Distance in m", lblY="Gear",dD=driver_dict, dO=driverOne, dT=driverTwo)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.header("RPM")
        fig = load_q(session, telX="Distance", telY="RPM", lblX="Distance in m", lblY="RPM",dD=driver_dict, dO=driverOne, dT=driverTwo)
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        st.header("Speed")
        fig = load_q(session, telX="Distance", telY="Speed", lblX="Distance in m", lblY="Speed in km/h", dD=driver_dict, dO=driverOne, dT=driverTwo)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    tab1, tab2 = st.tabs(["Bahrain", "Jeddah"])

    with tab1:
        st.header("Bahrain Grand Prix")
        draw_chart(fastf1.get_session(2023, 'Bahrain Grand Prix', 'Q'))

    with tab2:
        st.header("Jeddah Grand Prix")
        draw_chart(fastf1.get_session(2023, 'Jeddah Grand Prix', 'Q'))

    
