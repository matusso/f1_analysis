import fastf1
import streamlit as st
import matplotlib.pyplot as plt
from race import get_info
import pandas as pd

def get_stats(session):
    session.load(laps=True, weather=True, telemetry=True)
    laps = session.laps

    driver_dict = {}

    for d in session.drivers:
        driver = session.get_driver(d)
        driver_dict[driver['FullName']] = [driver['Abbreviation'], driver['TeamColor']]

    col1, col2 = st.columns(2)
    with col1:
        driverOne = st.selectbox('Select driver #1', driver_dict.keys(), key='selectboxDriver#1')

        numLaps = len(laps.pick_driver(driver_dict[driverOne][0]))
        bestLapNumberOne = int(laps.pick_driver(driver_dict[driverOne][0]).pick_fastest()['LapNumber'])
        bestLapCheckboxOne = st.checkbox('Best Lap', key='bestlap1checkboxStats')

        defaultLap = 1
        disabled = False
        if bestLapCheckboxOne == True:
            defaultLap = bestLapNumberOne
            disabled = True
       
        lapNumberOne = st.slider('Lap', 1, numLaps, defaultLap, key='lap#1s', disabled=disabled)
        lapOne = get_info(laps, lapNumber=lapNumberOne, driverAbbreviation=driver_dict[driverOne][0])

    with col2:
        driverTwo = st.selectbox('Select driver #2', driver_dict.keys(), key='selectboxDriver#2')
        numLaps = len(laps.pick_driver(driver_dict[driverTwo][0]))
        bestLapNumberTwo = int(laps.pick_driver(driver_dict[driverTwo][0]).pick_fastest()['LapNumber'])
        
        bestLapCheckboxTwo = st.checkbox('Best Lap', key='bestlap2checkboxStats')
        
        defaultLap = 1
        disabled = False
        if bestLapCheckboxTwo == True:
            defaultLap = bestLapNumberTwo
            disabled = True
        
        lapNumberTwo = st.slider('Lap', 1, numLaps, defaultLap, key='lap#2s', disabled=disabled)  
        lapTwo = get_info(laps, lapNumber=lapNumberTwo, driverAbbreviation=driver_dict[driverTwo][0])
    
    df = pd.DataFrame()
    df2 = df.append(lapOne)
#    st.write(df2.head())
    df2.rename(columns={'0': 'AAA'}, inplace=True)
  #  df3 = pd.DataFrame()
  #  df4 = df3.append(lapTwo)
   # df2.merge(df4)
    st.dataframe(df2.T, use_container_width=True)

   # st.dataframe(result)

     #   weatherTwo = lapTwo.get_weather_data()
       