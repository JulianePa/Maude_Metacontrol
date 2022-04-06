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
    last_space_index = -1
    for i in range(len(string)):
        if string[i] == '(':
            open_parenthesis += 1
        elif string[i] == ')':
            open_parenthesis -= 1
        elif string[i] == ' ' and open_parenthesis == 0:
            sub_string = string[last_space_index+1:i].replace(' ','')
            if sub_string != '':
                splitted.append(retrieve_function(sub_string))
            last_space_index = i

    sub_string = string[last_space_index+1:].replace(' ','')
    if sub_string != '':
        splitted.append(retrieve_function(sub_string.rstrip(',')))
    return splitted

def get_data_from_path(path, retrieve_function = retrieve_float):
    file = open(path, 'r')
    raw_data = file.read()
    raw_data = raw_data.replace('\n','')
    splitted_data = get_data_from_string(raw_data, retrieve_function)
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

def metacontrol_plot_background(axs, switch_points, data_lenght):
    for i in range(len(switch_points)):
        # axs.axvline(x = switch_points[i][0], color = 'k', linestyle = '--')

        end_block = switch_points[i+1][0] if i != len(switch_points) - 1 else data_lenght-1
        color = 'lightgoldenrodyellow' if switch_points[i][1] == "Eco" else 'lavender'
        axs.axvspan(switch_points[i][0], end_block, facecolor=color, alpha=1)


def main():
    comfort_temp_path = 'ComfortTempLog.txt'
    comfort_aq_path = 'ComfortAirqualityLog.txt'

    eco_temp_path = 'EcoTempLog.txt'
    eco_aq_path = 'EcoAirqualityLog.txt'

    meta_temp_path = 'MetaTempLog.txt'
    meta_aq_path = 'MetaAirqualityLog.txt'
    meta_controllers_path = 'MetaChangeLog.txt'


    comfort_temp_data = get_data_from_path(comfort_temp_path)
    comfort_aq_data = get_data_from_path(comfort_aq_path)
    comfort_temp_violation = calculate_violations(comfort_temp_data, 'temp')
    comfort_aq_violation = calculate_violations(comfort_aq_data, 'aq')
    print('Comfort number temp violation: ',comfort_temp_violation[0], ' number AQ violation: ',comfort_aq_violation[0], ' total number of violation: ', comfort_temp_violation[0]+comfort_aq_violation[0])
    print('Comfort amount temp violation: ',comfort_temp_violation[1], ' amount AQ violation: ',comfort_aq_violation[1], ' total amount of violation: ', comfort_temp_violation[1]+comfort_aq_violation[1])
    print('-------------')

    eco_temp_data = get_data_from_path(eco_temp_path)
    eco_aq_data = get_data_from_path(eco_aq_path)
    eco_temp_violation = calculate_violations(eco_temp_data, 'temp')
    eco_aq_violation = calculate_violations(eco_aq_data, 'aq')
    print('Eco temp number violation: ',eco_temp_violation[0], ' number AQ violation: ',eco_aq_violation[0], ' total number of violation: ', eco_temp_violation[0]+eco_aq_violation[0])
    print('Eco temp amount violation: ',eco_temp_violation[1], ' amount AQ violation: ',eco_aq_violation[1], ' total amount of violation: ', eco_temp_violation[1]+eco_aq_violation[1])
    print('-------------')

    meta_temp_data = get_data_from_path(meta_temp_path)
    meta_aq_data = get_data_from_path(meta_aq_path)
    meta_temp_violation = calculate_violations(meta_temp_data, 'temp')
    meta_aq_violation = calculate_violations(meta_aq_data, 'aq')
    print('Metacontrol number temp violation: ',meta_temp_violation[0], ' number AQ violation: ',meta_aq_violation[0], ' total number of violation: ', meta_temp_violation[0]+meta_aq_violation[0])
    print('Metacontrol amount temp violation: ',meta_temp_violation[1], ' amount AQ violation: ',meta_aq_violation[1], ' total amount of violation: ', meta_temp_violation[1]+meta_aq_violation[1])

    switch_points = get_data_from_path(meta_controllers_path, retrieve_string)
    # print(meta_controllers_switch)

    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Smart Home World')

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

    metacontrol_plot_background(axs[2, 0], switch_points, len(meta_temp_data))
    axs[2, 0].set_title("Meta controller temperature")
    axs[2, 0].plot(meta_temp_data)
    axs[2, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[2, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[2, 0].axhline(y = 22, color = 'k', linestyle = '--')

    metacontrol_plot_background(axs[2, 1], switch_points, len(meta_aq_data))
    axs[2, 1].set_title("Meta controller air quality")
    axs[2, 1].plot(meta_aq_data, 'r')
    axs[2, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[2, 1].axhline(y = 0, color = 'k', linestyle = '--')



    plt.show()

if __name__ == "__main__":
    main()
