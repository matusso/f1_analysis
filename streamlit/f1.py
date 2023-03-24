import streamlit as st

import matplotlib.pyplot as plt
import fastf1.plotting
import pandas as pd
from fastf1 import plotting, utils

fastf1.Cache.enable_cache('/tmp')  # replace with your cache directory

# enable some matplotlib patches for plotting timedelta values and load
# FastF1's default color scheme
fastf1.plotting.setup_mpl()


def load_q(session, telX, telY, lblX, lblY, dD, dO, dT):
    driver_dict = dD
    driverOne = dO
    driverTwo = dT

    ver_lap = session.laps.pick_driver(driver_dict[driverOne][0]).pick_fastest()
    ham_lap = session.laps.pick_driver(driver_dict[driverTwo][0]).pick_fastest()

    ver_tel = ver_lap.get_car_data().add_distance()
    ham_tel = ham_lap.get_car_data().add_distance()

    fig, ax = plt.subplots()
    if driver_dict[driverOne][1] == driver_dict[driverTwo][1]:
        driver_dict[driverTwo][1] = "FFFFFF"

    ax.plot(ver_tel[telX], ver_tel[telY], color='#'+driver_dict[driverOne][1], label=driver_dict[driverOne][0])
    ax.plot(ham_tel[telX], ham_tel[telY], color='#'+driver_dict[driverTwo][1], label=driver_dict[driverTwo][0])

    #ax.set_xlabel('Distance in m')
    #ax.set_ylabel('Speed in km/h')
    ax.set_xlabel(lblX)
    ax.set_ylabel(lblY)

    return fig
    

def draw_chart(session):
    session.load(telemetry=True, weather=True)
    driver_dict = {}

    for d in session.drivers:
        driver = session.get_driver(d)
        #print(driver)
        driver_dict[driver['FullName']] = [driver['Abbreviation'], driver['TeamColor']]

    col1, col2 = st.columns(2)
    with col1:
        driverOne = st.selectbox('Select driver #1', driver_dict.keys())
    
    with col2:
        driverTwo = st.selectbox('Select driver #2', driver_dict.keys())

    st.header("Speed")
    fig = load_q(session, telX="Distance", telY="Speed", lblX="Distance in m", lblY="Speed in km/h", dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Gear")
    fig = load_q(session, telX="Distance", telY="nGear", lblX="Distance in m", lblY="Gear",dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("RPM")
    fig = load_q(session, telX="Distance", telY="RPM", lblX="Distance in m", lblY="RPM",dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Throttle")
    fig = load_q(session, telX="Distance", telY="Throttle", lblX="Distance in m", lblY="Throttle",dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Brake")
    fig = load_q(session, telX="Distance", telY="Brake", lblX="Distance in m", lblY="Brake",dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("DRS")
    fig = load_q(session, telX="Distance", telY="DRS", lblX="Distance in m", lblY="DRS",dD=driver_dict, dO=driverOne, dT=driverTwo)
    st.plotly_chart(fig, use_container_width=True)




if __name__ == '__main__':
    st.set_page_config(page_title="F1 Analysis (by matusso)", layout="wide")

    col1, col2 = st.columns(2)
    with col1:
        selectedYear = st.selectbox('Year', [2018, 2019, 2020, 2021, 2022, 2023])

    schedule = fastf1.get_event_schedule(selectedYear)
    round_dict = {}
    for index, row in schedule.iterrows():
        if row["RoundNumber"] > 0:
            round_dict[row["Location"]] = row["RoundNumber"] 
    
    with col2:
        circuitName = st.selectbox('Select Circuit', round_dict.keys())

    print(schedule.get_event_by_round(round_dict[circuitName]))
    st.header(str(selectedYear) + "/" + circuitName)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race"])

    with tab4:
        draw_chart(fastf1.get_session(selectedYear, circuitName, 'Q'))

#with tab5:
        #race_results(fastf1.get_session(selectedYear, circuitName, 'R'))

    
