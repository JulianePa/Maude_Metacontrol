class Controller:
    def __init__(self, temp_low, temp_high, aq_low):
        self.temp_low = temp_low
        self.temp_high = temp_high
        self.aq_low = aq_low

    def is_morning(self, time):
        print((time%(24) >= 6) and (time%(24) <= 12))
        return (time%(24) >= 6) and (time%(24) <= 12)

class ComfortController(Controller):
    def __init__(self, temp_low, temp_high, aq_low):
        super().__init__(temp_low, temp_high, aq_low)

    def actuate(self, temp, aq, time, window):
        morning = self.is_morning(time)
        new_state = dict()
        if temp <= self.temp_low and morning:
            new_state["heater"] = "FAIRLY HOT"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp <= self.temp_low and not morning:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp > self.temp_low and temp <= self.temp_high and aq > self.aq_low and morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp > self.temp_low and temp <= self.temp_high and aq > self.aq_low and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window != "OPEN" and morning:
            new_state["heater"] = "FAIRLY HOT"
            new_state["water_heater"] = "ON"
            new_state["window"] = "HALF OPEN"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window != "OPEN" and not morning:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "HALF OPEN"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window == "OPEN" and morning:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "ON"
            new_state["window"] = "OPEN"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window == "OPEN" and not morning:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "OPEN"
        elif temp > self.temp_high and morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "OPEN"
        elif temp > self.temp_high and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "OPEN"

        return new_state

class EcoController(Controller):
    def __init__(self, temp_low, temp_high, aq_low):
        super().__init__(temp_low, temp_high, aq_low)

    def actuate(self, temp, aq, time, window):
        morning = morning = self.is_morning(time)
        new_state = dict()
        if temp <= self.temp_low and aq > self.aq_low:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "ON"
            new_state["window"] = "HALF OPEN"
        elif temp <= self.temp_low and aq <= self.aq_low and morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "HALF OPEN"
        elif temp <= self.temp_low and aq <= self.aq_low and not morning:
            new_state["heater"] = "VERY HOT"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "HALF OPEN"
        elif temp > self.temp_low and temp <= self.temp_high and aq > self.aq_low and morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp > self.temp_low and temp <= self.temp_high and aq > self.aq_low and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "CLOSED"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window != "OPEN":
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "HALF OPEN"
        elif temp > self.temp_low and temp <= self.temp_high and aq <= self.aq_low and window == "OPEN":
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "OPEN"
        elif temp > self.temp_high and morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "ON"
            new_state["window"] = "OPEN"
        elif temp > self.temp_high and aq > self.aq_low and window != "OPEN" and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "HALF OPEN"
        elif temp > self.temp_high and aq > self.aq_low and window == "OPEN" and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "OPEN"
        elif temp > self.temp_high and aq <= self.aq_low and not morning:
            new_state["heater"] = "OFF"
            new_state["water_heater"] = "OFF"
            new_state["window"] = "OPEN"

        return new_state
