#!/usr/bin/env python3

from world import *
import matplotlib.pyplot as plt
from controller import ComfortController, EcoController

initial_world_state = {
    "time":0,
    "temperature": 19,
    "air_quality": 1,
    "heater": "OFF",
    "water_heater": "OFF",
    "window": "CLOSED"}

heater_config = {
    "name": "heater",
    "OFF": (0,0),
    "FAIRLY HOT": (1, -0.5),
    "VERY HOT": (2, -1)
}

water_heater_config = {
    "name": "water_heater",
    "OFF": (0,0),
    "ON": (0.5, -0.25),
}

window_config = {
    "name": "window",
    "OPEN": (-1, 2),
    "HALF OPEN": (-0.5, 1),
    "CLOSED": (0, 0)
}
# heater_config = {
#     "name": "heater",
#     "OFF": (0,0),
#     "FAIRLY HOT": (0.016, -0.008),
#     "VERY HOT": (0.032, -0.016)
# }
#
# water_heater_config = {
#     "name": "water_heater",
#     "OFF": (0,0),
#     "ON": (0.008, -0.004),
# }
#
# window_config = {
#     "name": "window",
#     "OPEN": (-0.016, 0.032),
#     "HALF OPEN": (-0.008, 0.016),
#     "CLOSED": (0, 0)
# }

actuators_config = {
    "heater": heater_config,
    "water_heater": water_heater_config,
    "window": window_config
}

temp_low = 18.5
temp_high = 21.5
aq_low = 0.5

smart_home_world_comfort = World(initial_world_state, actuators_config)
comfort_controller = ComfortController(temp_low, temp_high, aq_low)
smart_home_world_comfort.controller = comfort_controller

smart_home_world_eco = World(initial_world_state, actuators_config)
eco_controller = EcoController(temp_low, temp_high, aq_low)
smart_home_world_eco.controller = eco_controller

time_steps = 100

for t in range(0,time_steps):
    smart_home_world_comfort.step_world()
    smart_home_world_eco.step_world()

# print(smart_home_world.world_states)

temperature_values_comfort = [s["temperature"] for s in smart_home_world_comfort.world_states]
air_quality_values_comfort = [s["air_quality"] for s in smart_home_world_comfort.world_states]

temperature_values_eco = [s["temperature"] for s in smart_home_world_eco.world_states]
air_quality_values_eco = [s["air_quality"] for s in smart_home_world_eco.world_states]

fig, axs = plt.subplots(2, 2)
fig.suptitle('Smart Home World')

axs[0, 0].set_title("Comfort controller temperature")
axs[0, 0].plot(temperature_values_comfort)
axs[0, 0].set(xlabel='Time step', ylabel='Temperature')
axs[0, 0].axhline(y = 18, color = 'k', linestyle = '--')
axs[0, 0].axhline(y = 22, color = 'k', linestyle = '--')

axs[0, 1].set_title("Comfort controller air quality")
axs[0, 1].plot(air_quality_values_comfort, 'r')
axs[0, 1].set(xlabel='Time step', ylabel='Air quality')
axs[0, 1].axhline(y = 0, color = 'k', linestyle = '--')

axs[1, 0].set_title("Eco controller temperature")
axs[1, 0].plot(temperature_values_eco)
axs[1, 0].set(xlabel='Time step', ylabel='Temperature')
axs[1, 0].axhline(y = 18, color = 'k', linestyle = '--')
axs[1, 0].axhline(y = 22, color = 'k', linestyle = '--')

axs[1, 1].set_title("Eco controller air quality")
axs[1, 1].plot(air_quality_values_eco, 'r')
axs[1, 1].set(xlabel='Time step', ylabel='Air quality')
axs[1, 1].axhline(y = 0, color = 'k', linestyle = '--')

plt.show()
