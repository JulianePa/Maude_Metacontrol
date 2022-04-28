import matplotlib.pyplot as plt

def retrieve_string(string):
    sub_string = string.strip('() ').replace('\n','')
    sub_string = sub_string.split(',')
    return (int(sub_string[0]), sub_string[1])

def retrieve_float(string):
    return float(retrieve_string(string)[1])

#split by space if not inside parenthesis or nested parenthesis, remove new line
# spaces, trailing comma. Split data and convert to int/float
def get_data_from_string(string, retrieve_function):
    open_parenthesis = 0
    splitted = []
    last_open_parenthesis_index = 0
    string = string.replace(' ', '')
    for i in range(len(string)):
        if string[i] == '(':
            open_parenthesis += 1
            last_open_parenthesis_index = i
        elif string[i] == ')':
            open_parenthesis -= 1
            sub_string = string[last_open_parenthesis_index+1:i]
            if sub_string != '':
                splitted.append(retrieve_function(sub_string))
            last_close_parenthesis_index = i

    sub_string = string[last_close_parenthesis_index+1:]
    if sub_string != '':
        splitted.append(retrieve_function(sub_string.rstrip(',')))
    return splitted

def get_data_from_path(path, retrieve_function = retrieve_float, time_steps=None):
    file = open(path, 'r')
    raw_data = file.read()
    raw_data = raw_data.replace('\n','')
    splitted_data = get_data_from_string(raw_data, retrieve_function)
    if time_steps != None:
        splitted_data = splitted_data[0:time_steps]
    return splitted_data

def calculate_violations(data, qa):
    violation_times_count = 0
    violation_amount = 0
    violation_expression = None
    if qa == 'aq':
        violation_expression = lambda d : d < 0
        amount_violation_expression = lambda d : abs(d)
    elif qa== 'temp':
        violation_expression = lambda d : d < 18 or d >22
        amount_violation_expression = lambda d: (18 - d) if d < 18 else ((d-22) if d > 22 else 0)

    for d in data:
        if violation_expression(d):
            violation_times_count += 1
            violation_amount += amount_violation_expression(d)

    return (violation_times_count, round(violation_amount,3))

def metacontrol_plot_background(axs, switch_points, data_lenght, time_steps=None):
    legend_count = []
    if time_steps!=None:
        data_lenght=time_steps
        for i in range(len(switch_points)):
            if time_steps!=None and switch_points[i][0] > time_steps:
                switch_points = switch_points[0:i]
                break

    for i in range(len(switch_points)):
        # axs.axvline(x = switch_points[i][0], color = 'k', linestyle = '--')
        end_block = switch_points[i+1][0] if i != len(switch_points) - 1 else data_lenght-1
        color = 'lightgoldenrodyellow' if switch_points[i][1] == "Eco" else 'lavender'
        span = axs.axvspan(switch_points[i][0], end_block, facecolor=color, alpha=1)
        if len(legend_count)<2 and switch_points[i][1] not in legend_count:
            span.set_label(switch_points[i][1])
            legend_count.append(switch_points[i][1])
    axs.legend(loc='upper right')

def write_log_to_file(path, filename, data):
    file = open(path+filename, 'w+')
    file.write(data)

def process_maude_log(path):
     file = open(path, 'r')
     raw_data = file.read()

     # order: comfort, eco, metacontrol
     controllers_log = raw_data.split("==========================================")[1:]
     controllers_name = ["ComfortController","EcoController","Metacontrol"]
     for (controller_log, controller_name) in zip(controllers_log, controllers_name):
         init_index = controller_log.find("homeClock")
         temp_log_index = controller_log.find("TempLog:", init_index)
         aq_log_index = controller_log.find("AqLog:", temp_log_index)
         final_index = controller_log.find(">", aq_log_index)

         temp_log = controller_log[temp_log_index+8:aq_log_index]
         aq_log = controller_log[aq_log_index+6:final_index]

         try:
             metacontrol_index = controller_log.index("MetaLog")
             final_metacontrol_index = controller_log.index(">", metacontrol_index)
             metacontrol_log = "(0, Eco)" + controller_log[metacontrol_index+8: final_metacontrol_index]
             write_log_to_file('logs/', controller_name+"ChangeLog.txt", metacontrol_log.replace('\n',''))
         except ValueError:
             pass

         write_log_to_file('logs/', controller_name+"TempLog.txt", temp_log.replace('\n',''))
         write_log_to_file('logs/', controller_name+"AirQualityLog.txt", aq_log.replace('\n',''))

def main():

    time_steps = 200

    maude_log_path = 'logs/maude_log'
    process_maude_log(maude_log_path)

    comfort_temp_path = 'logs/ComfortControllerTempLog.txt'
    comfort_aq_path = 'logs/ComfortControllerAirQualityLog.txt'

    eco_temp_path = 'logs/EcoControllerTempLog.txt'
    eco_aq_path = 'logs/EcoControllerAirQualityLog.txt'

    meta_temp_path = 'logs/MetacontrolTempLog.txt'
    meta_aq_path = 'logs/MetacontrolAirQualityLog.txt'
    meta_controllers_path = 'logs/MetacontrolChangeLog.txt'


    comfort_temp_data = get_data_from_path(comfort_temp_path, time_steps=time_steps)
    comfort_aq_data = get_data_from_path(comfort_aq_path, time_steps=time_steps)
    comfort_temp_violation = calculate_violations(comfort_temp_data, 'temp')
    comfort_aq_violation = calculate_violations(comfort_aq_data, 'aq')
    print('Comfort number temp violation: ',comfort_temp_violation[0], ' number AQ violation: ',comfort_aq_violation[0], ' total number of violation: ', comfort_temp_violation[0]+comfort_aq_violation[0])
    print('Comfort amount temp violation: ',comfort_temp_violation[1], ' amount AQ violation: ',comfort_aq_violation[1], ' total amount of violation: ', comfort_temp_violation[1]+comfort_aq_violation[1])
    print('-------------')

    eco_temp_data = get_data_from_path(eco_temp_path, time_steps=time_steps)
    eco_aq_data = get_data_from_path(eco_aq_path, time_steps=time_steps)
    eco_temp_violation = calculate_violations(eco_temp_data, 'temp')
    eco_aq_violation = calculate_violations(eco_aq_data, 'aq')
    print('Eco temp number violation: ',eco_temp_violation[0], ' number AQ violation: ',eco_aq_violation[0], ' total number of violation: ', eco_temp_violation[0]+eco_aq_violation[0])
    print('Eco temp amount violation: ',eco_temp_violation[1], ' amount AQ violation: ',eco_aq_violation[1], ' total amount of violation: ', eco_temp_violation[1]+eco_aq_violation[1])
    print('-------------')

    meta_temp_data = get_data_from_path(meta_temp_path, time_steps=time_steps)
    meta_aq_data = get_data_from_path(meta_aq_path, time_steps=time_steps)
    meta_temp_violation = calculate_violations(meta_temp_data, 'temp')
    meta_aq_violation = calculate_violations(meta_aq_data, 'aq')
    print('Metacontrol number temp violation: ',meta_temp_violation[0], ' number AQ violation: ',meta_aq_violation[0], ' total number of violation: ', meta_temp_violation[0]+meta_aq_violation[0])
    print('Metacontrol amount temp violation: ',meta_temp_violation[1], ' amount AQ violation: ',meta_aq_violation[1], ' total amount of violation: ', meta_temp_violation[1]+meta_aq_violation[1])

    switch_points = get_data_from_path(meta_controllers_path, retrieve_string)

    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Smart Home')

    axs[0, 0].set_title("Comfort controller temperature")
    axs[0, 0].plot(comfort_temp_data)
    axs[0, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[0, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[0, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[0, 1].set_title("Comfort controller air quality")
    axs[0, 1].plot(comfort_aq_data, 'r')
    axs[0, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[0, 1].axhline(y = 0, color = 'k', linestyle = '--')

    axs[1, 0].set_title("Eco controller temperature")
    axs[1, 0].plot(eco_temp_data)
    axs[1, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[1, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[1, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[1, 1].set_title("Eco controller air quality")
    axs[1, 1].plot(eco_aq_data, 'r')
    axs[1, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[1, 1].axhline(y = 0, color = 'k', linestyle = '--')

    metacontrol_plot_background(axs[2, 0], switch_points, len(meta_temp_data), time_steps)
    axs[2, 0].set_title("Meta controller temperature")
    axs[2, 0].plot(meta_temp_data)
    axs[2, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[2, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[2, 0].axhline(y = 22, color = 'k', linestyle = '--')

    metacontrol_plot_background(axs[2, 1], switch_points, len(meta_aq_data), time_steps)
    axs[2, 1].set_title("Meta controller air quality")
    axs[2, 1].plot(meta_aq_data, 'r')
    axs[2, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[2, 1].axhline(y = 0, color = 'k', linestyle = '--')

    plt.show()

if __name__ == "__main__":
    main()
