#!/usr/bin/env python3
import fastf1 as ff1

ff1.Cache.enable_cache('../../cache')  

quali = ff1.get_session(2021, 'French Grand Prix', 'Q')
laps = quali.load_laps()

print(laps)