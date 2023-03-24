import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps

def qualification_results(session):
    session.load()
    drivers = pd.unique(session.laps['Driver'])
    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
    #print(fastest_laps)

    fastest_laps['LapTime'] = pd.to_timedelta(fastest_laps['LapTime']).apply(lambda x: str(x))
    fastest_laps['LapTimeDelta'] = pd.to_timedelta(fastest_laps['LapTimeDelta']).apply(lambda x: str(x))

    results = session.results.copy()
    results['Q1s'] = pd.to_timedelta(results['Q1']).apply(lambda x: str(x))
    results['Q2s'] = pd.to_timedelta(results['Q2']).apply(lambda x: str(x))
    results['Q3s'] = pd.to_timedelta(results['Q3']).apply(lambda x: str(x))
    results['Times'] = pd.to_timedelta(results['Time']).apply(lambda x: str(x))
    results['PositionS'] = results['Position'].astype(int)

    st.header("Qualifying results")
    st.table(results[['FullName', 'TeamName', 'Q1s', 'Q2s', 'Q3s', 'PositionS']])