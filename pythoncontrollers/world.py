class World:
    def __init__(self, inititial_states, actuators_config):
        self.world_states = list()
        # self.world_states.append(WorldState(inititial_states))
        self.world_states.append(inititial_states)

        # dict heater: ActuatorConfig, water_heater: ActuatorConfig,
        # window: ActuatorConfig
        self.actuators_config = actuators_config #dict{name: , "Off":(dt,daq),...}

        self.controller = None

    def step_world(self):
        current_state = self.world_states[-1]
        # new_state = WorldState()
        new_state = dict()
        new_state["time"] = current_state["time"] + 1
        delta_temperature = 0
        delta_airquality = 0

        # Apply world dynamics
        if (current_state["heater"] == "OFF" and
            current_state["water_heater"] == "OFF" and
            current_state["window"] == "CLOSED"):

            delta_temperature = -0.25
            delta_airquality = -0.25
        else:
            for actuator in self.actuators_config.values():
                actuator_name = actuator["name"]
                actuator_status = current_state[actuator_name]
                delta_temperature += actuator[actuator_status][0]
                delta_airquality += actuator[actuator_status][1]

        new_state["temperature"] = current_state["temperature"] + delta_temperature
        new_state["air_quality"] = current_state["air_quality"] + delta_airquality

        # Apply controller
        if self.controller == None:
            new_state["heater"] = current_state["heater"]
            new_state["water_heater"] = current_state["water_heater"]
            new_state["window"] = current_state["window"]
        else:
            new_state_aux = self.controller.actuate(new_state["temperature"],
                                                    new_state["air_quality"],
                                                    current_state["time"],
                                                    current_state["window"])
            new_state["heater"] = new_state_aux["heater"]
            new_state["water_heater"] = new_state_aux["water_heater"]
            new_state["window"] = new_state_aux["window"]

        self.world_states.append(new_state)


    def set_actuators_status(self):
        pass

    def get_sensor_readings(self):
        pass


# class WorldState:
#     def __init__(self):
#         self.time = None
#
#         self.temperature = None
#         self.air_quality = None
#
#         self.heater = None
#         self.water_heater = None
#         self.window = None
#
#     def __init__(self, states):
#         self.time = states["time"]
#
#         self.temperature = states["temperature"]
#         self.air_quality = states["air_quality"]
#
#         self.heater = states["heater"]
#         self.water_heater = states["water_heater"]
#         self.window = states["window"]
#
# class ActuatorConfig:
#     def __init__(self, name, effects_dict):
#         self.name = name
#         self.effects_dict = effects_dict
