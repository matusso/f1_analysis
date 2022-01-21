import matplotlib.pyplot as plt
import fastf1.plotting


fastf1.Cache.enable_cache('f1cache')  # replace with your cache directory

# enable some matplotlib patches for plotting timedelta values and load
# FastF1's default color scheme
fastf1.plotting.setup_mpl()

# load a session and its telemetry data
quali = fastf1.get_session(2021, 'AbuDhabi', 'Q')
laps = quali.load_laps(with_telemetry=True)

ver_lap = laps.pick_driver('VER').pick_fastest()
ham_lap = laps.pick_driver('HAM').pick_fastest()

ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()

rbr_color = fastf1.plotting.team_color('RBR')
mer_color = fastf1.plotting.team_color('MER')

fig, ax = plt.subplots(3, 2, sharex=True)

ax[0, 0].set_title("Speed")
ax[0, 0].plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='VER')
ax[0, 0].plot(ham_tel['Distance'], ham_tel['Speed'], color=mer_color, label='HAM')

ax[1, 0].set_title("Throttle")
ax[1, 0].plot(ver_tel['Distance'], ver_tel['Throttle'], color=rbr_color, label='VER')
ax[1, 0].plot(ham_tel['Distance'], ham_tel['Throttle'], color=mer_color, label='HAM')
ax[1, 0].sharex(ax[0, 0])

ax[0, 1].set_title("Brake")
ax[0, 1].plot(ver_tel['Distance'], ver_tel['Brake'], color=rbr_color, label='VER')
ax[0, 1].plot(ham_tel['Distance'], ham_tel['Brake'], color=mer_color, label='HAM')
ax[0, 1].sharex(ax[0, 0])

ax[1, 1].set_title("Gear")
ax[1, 1].plot(ver_tel['Distance'], ver_tel['nGear'], color=rbr_color, label='VER')
ax[1, 1].plot(ham_tel['Distance'], ham_tel['nGear'], color=mer_color, label='HAM')
ax[1, 1].sharex(ax[0, 0])

ax[2, 0].set_title("RPM")
ax[2, 0].plot(ver_tel['Distance'], ver_tel['RPM'], color=rbr_color, label='VER')
ax[2, 0].plot(ham_tel['Distance'], ham_tel['RPM'], color=mer_color, label='HAM')
ax[2, 0].sharex(ax[0, 0])

ax[2, 1].set_title("Delta time")
delta_time, ref_tel, compare_tel = fastf1.utils.delta_time(ver_lap, ham_lap)
ax[2, 1].plot(ref_tel['Distance'], ref_tel['Speed'], color=rbr_color)
ax[2, 1].plot(compare_tel['Distance'], compare_tel['Speed'], color=mer_color)
twin = ax[2, 1].twinx()
twin.plot(ref_tel['Distance'], delta_time, '--', color='white')
twin.set_ylabel("<-- Ver ahead | Ham ahead -->")


fig.tight_layout()


#ax.set_xlabel('Distance in m')
#ax.set_ylabel('Speed in km/h')

#ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{quali.weekend.name} {quali.weekend.year} Qualifying")

plt.show()
fig.savefig('fastest_lap_compare_ver_ham.png')