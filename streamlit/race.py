import fastf1
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def get_info(laps, lapNumber, driverAbbreviation):
    for index, row in laps.iterrows():
        if row['LapNumber'] == lapNumber and row['Driver'] == driverAbbreviation:
            return row

def load_telemetry(lapOne, lapTwo, driver_dict, driverOne, driverTwo, telX, telY, lblX, lblY): 
    tel1 = lapOne.get_car_data().add_distance()
    tel2 = lapTwo.get_car_data().add_distance()

    fig, ax = plt.subplots()
    if driver_dict[driverOne][1] == driver_dict[driverTwo][1]:
        driver_dict[driverTwo][1] = "FFFFFF"

    ax.plot(tel1[telX], tel1[telY], color='#'+driver_dict[driverOne][1], label=driver_dict[driverOne][0])
    ax.plot(tel2[telX], tel2[telY], color='#'+driver_dict[driverTwo][1], label=driver_dict[driverTwo][0])


    ax.set_xlabel(lblX)
    ax.set_ylabel(lblY)

    return fig

def race_lap_telemetry(session):
    session.load(laps=True, weather=True, telemetry=True)
    laps = session.laps
    driver_dict = {}

    for d in session.drivers:
        driver = session.get_driver(d)
        driver_dict[driver['FullName']] = [driver['Abbreviation'], driver['TeamColor']]

    col1, col2 = st.columns(2)
    with col1:
        driverOne = st.selectbox('Select driver #1', driver_dict.keys())

        numLaps = len(laps.pick_driver(driver_dict[driverOne][0]))
        bestLapNumberOne = int(laps.pick_driver(driver_dict[driverOne][0]).pick_fastest()['LapNumber'])
        bestLapCheckboxOne = st.checkbox('Best Lap', key='bestlap1checkbox')

        defaultLap = 1
        disabled = False
        if bestLapCheckboxOne == True:
            defaultLap = bestLapNumberOne
            disabled = True
       
        lapNumberOne = st.slider('Lap', 1, numLaps, defaultLap, key='lap#1', disabled=disabled)

        lapOne = get_info(laps, lapNumber=lapNumberOne, driverAbbreviation=driver_dict[driverOne][0])
        weatherOne = lapOne.get_weather_data()
        m1, m2, m3 = st.columns(3)
    
        sec1 = pd.to_timedelta(lapOne['Sector1Time']).total_seconds() 
        sec2 = pd.to_timedelta(lapOne['Sector2Time']).total_seconds() 
        sec3 = pd.to_timedelta(lapOne['Sector2Time']).total_seconds() 

        m1.metric("Sector 1", str(sec1))
        m2.metric("Sector 2", str(sec2))
        m3.metric("Sector 3", str(sec3))

    with col2:
        driverTwo = st.selectbox('Select driver #2', driver_dict.keys())
        numLaps = len(laps.pick_driver(driver_dict[driverTwo][0]))
        bestLapNumberTwo = int(laps.pick_driver(driver_dict[driverTwo][0]).pick_fastest()['LapNumber'])
        
        bestLapCheckboxTwo = st.checkbox('Best Lap', key='bestlap2checkbox')
        
        defaultLap = 1
        disabled = False
        if bestLapCheckboxTwo == True:
            defaultLap = bestLapNumberTwo
            disabled = True
        
        lapNumberTwo = st.slider('Lap', 1, numLaps, defaultLap, key='lap#2', disabled=disabled)  
        lapTwo = get_info(laps, lapNumber=lapNumberTwo, driverAbbreviation=driver_dict[driverTwo][0])
        weatherTwo = lapTwo.get_weather_data()
        m1, m2, m3 = st.columns(3)
   #     m1.metric("AirTemp", weatherTwo['AirTemp'], weatherTwo['AirTemp'] - weatherOne['AirTemp'])
    #    m2.metric("TrackTemp", weatherTwo['TrackTemp'], weatherTwo['TrackTemp'] - weatherOne['TrackTemp'])
    #    m3.metric("WindSpeed", weatherTwo['WindSpeed'], weatherTwo['WindSpeed'] - weatherOne['WindSpeed'])

        secT1 = pd.to_timedelta(lapTwo['Sector1Time']).total_seconds() 
        secT2 = pd.to_timedelta(lapTwo['Sector2Time']).total_seconds() 
        secT3 = pd.to_timedelta(lapTwo['Sector2Time']).total_seconds() 

        m1.metric("Sector 1", str(secT1), str(round(secT1 - sec1, 3)), delta_color="inverse")
        m2.metric("Sector 2", str(secT2), str(round(secT2 - sec2, 3)), delta_color="inverse")
        m3.metric("Sector 3", str(secT3), str(round(secT3 - sec3, 3)), delta_color="inverse")

        

    st.header("Speed")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="Speed", lblX="Distance in m", lblY="Speed in km/h", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Gear")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="nGear", lblX="Distance in m", lblY="Gear", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("RPM")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="RPM", lblX="Distance in m", lblY="RPM", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Throttle")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="Throttle", lblX="Distance in m", lblY="Throttle", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Brake")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="Brake", lblX="Distance in m", lblY="Brake", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    st.header("DRS")
    fig = load_telemetry(lapOne=lapOne, lapTwo=lapTwo, telX="Distance", telY="DRS", lblX="Distance in m", lblY="DRS", driver_dict=driver_dict, driverOne=driverOne, driverTwo=driverTwo)
    st.plotly_chart(fig, use_container_width=True)

    
