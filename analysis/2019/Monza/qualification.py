#!/usr/bin/env python3

from matplotlib import pyplot as plt
import fastf1 as ff1
from fastf1 import plotting

plotting.setup_mpl()

ff1.Cache.enable_cache('../../cache')
monza_quali = ff1.get_session(2019, 'Monza', 'Q')

laps = monza_quali.load_laps(with_telemetry=True)

fast_leclerc = laps.pick_driver('LEC').pick_fastest()
fast_hamilton = laps.pick_driver('HAM').pick_fastest()

lec_car_data = fast_leclerc.get_car_data()
ham_car_data = fast_hamilton.get_car_data()

t_lec = lec_car_data['Time']
t_ham = ham_car_data['Time']

vCarLec = lec_car_data['Speed']
vCarHam = ham_car_data['Speed']

vCarLecThrottle = lec_car_data['Throttle']
vCarHamThrottle = ham_car_data['Throttle']

vCarLecBrake = lec_car_data['Brake']
vCarHamBrake = ham_car_data['Brake']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t_lec, vCarLec, label='Lec')
ax.plot(t_ham, vCarHam, label='Ham')

ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')   
ax.set_title('Speed')

fig, bx = plt.subplots()
bx.plot(t_lec, vCarLecThrottle, label='Lec')
bx.plot(t_ham, vCarHamThrottle, label='Ham')

bx.set_xlabel('Time')
bx.set_ylabel('Throttle')   
bx.set_title('Throttle')

fig, cx = plt.subplots()
cx.plot(t_lec, vCarLecBrake, label='Lec')
cx.plot(t_ham, vCarHamBrake, label='Ham')

cx.set_xlabel('Time')
cx.set_ylabel('Brake')   
cx.set_title('Brake')

ax.legend()
bx.legend()
cx.legend()

plt.show()