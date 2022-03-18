class World:
    def __init__(self, inititial_states, actuators_config):
        self.world_states = list()
        # self.world_states.append(WorldState(inititial_states))
        self.world_states.append(inititial_states)

        # dict heater: ActuatorConfig, water_heater: ActuatorConfig,
        # window: ActuatorConfig
        self.actuators_config = actuators_config #dict{name: , "Off":(dt,daq),...}

        self.controller = None

    def get_world_temp_delta(self, time):
        day_time = time%24
        world_temp_delta = None
        if (day_time>=0 and day_time<6):
            world_temp_delta = -0.5
        elif (day_time>=6 and day_time <12) or (day_time>=18):
            world_temp_delta = -0.25
        elif (day_time>=12 and day_time <18):
            world_temp_delta = 0

        return world_temp_delta

    def step_world(self):
        current_state = self.world_states[-1]
        # new_state = WorldState()
        new_state = dict()
        new_state["time"] = current_state["time"] + 1
        delta_temperature = self.get_world_temp_delta(current_state["time"])
        delta_airquality = 0.00

        for actuator in self.actuators_config.values():
            actuator_name = actuator["name"]
            actuator_status = current_state[actuator_name]
            print("actuator ",actuator_name, " status " , actuator_status)
            delta_temperature += actuator[actuator_status][0]
            delta_airquality += actuator[actuator_status][1]

        new_state["temperature"] = round(current_state["temperature"] + round(delta_temperature, 2), 2)
        new_state["air_quality"] = round(current_state["air_quality"] + round(delta_airquality, 2), 2)

        # Apply controller
        if self.controller == None:
            new_state["heater"] = current_state["heater"]
            new_state["water_heater"] = current_state["water_heater"]
            new_state["window"] = current_state["window"]
        else:
            new_state_aux = self.controller.actuate(new_state["temperature"],
                                                    new_state["air_quality"],
                                                    new_state["time"],
                                                    current_state["window"])
            new_state["heater"] = new_state_aux["heater"]
            new_state["water_heater"] = new_state_aux["water_heater"]
            new_state["window"] = new_state_aux["window"]

        self.world_states.append(new_state)
