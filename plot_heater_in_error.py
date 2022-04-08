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

def main():
    hHerr_temp_path = 'HErrTempLog.txt'
    hHerr_aq_path = 'HErrAirqualityLog.txt'

    whErr_temp_path = 'HBrokenComfTempLog.txt'
    whErr_aq_path = 'HBrokenComfAirqualityLog.txt'

    wErr_temp_path = 'HBrokenEcoTempLog.txt'
    wErr_aq_path = 'HBrokenEcoAirqualityLog.txt'


    hHerr_temp_data = get_data_from_path(hHerr_temp_path)
    hHerr_aq_data = get_data_from_path(hHerr_aq_path)
    hHerr_temp_violation = calculate_violations(hHerr_temp_data, 'temp')
    hHerr_aq_violation = calculate_violations(hHerr_aq_data, 'aq')
    print('HeaterErr number temp violation: ',hHerr_temp_violation[0], ' number AQ violation: ',hHerr_aq_violation[0], ' total number of violation: ', hHerr_temp_violation[0]+hHerr_aq_violation[0])
    print('HeaterErr amount temp violation: ',hHerr_temp_violation[1], ' amount AQ violation: ',hHerr_aq_violation[1], ' total amount of violation: ', hHerr_temp_violation[1]+hHerr_aq_violation[1])
    print('-------------')

    whErr_temp_data = get_data_from_path(whErr_temp_path)
    whErr_aq_data = get_data_from_path(whErr_aq_path)
    whErr_temp_violation = calculate_violations(whErr_temp_data, 'temp')
    whErr_aq_violation = calculate_violations(whErr_aq_data, 'aq')
    print('Comfort temp number violation: ',whErr_temp_violation[0], ' number AQ violation: ',whErr_aq_violation[0], ' total number of violation: ', whErr_temp_violation[0]+whErr_aq_violation[0])
    print('Comfort temp amount violation: ',whErr_temp_violation[1], ' amount AQ violation: ',whErr_aq_violation[1], ' total amount of violation: ', whErr_temp_violation[1]+whErr_aq_violation[1])
    print('-------------')

    wErr_temp_data = get_data_from_path(wErr_temp_path)
    wErr_aq_data = get_data_from_path(wErr_aq_path)
    wErr_temp_violation = calculate_violations(wErr_temp_data, 'temp')
    wErr_aq_violation = calculate_violations(wErr_aq_data, 'aq')
    print('Eco number temp violation: ',wErr_temp_violation[0], ' number AQ violation: ',wErr_aq_violation[0], ' total number of violation: ', wErr_temp_violation[0]+wErr_aq_violation[0])
    print('Eco amount temp violation: ',wErr_temp_violation[1], ' amount AQ violation: ',wErr_aq_violation[1], ' total amount of violation: ', wErr_temp_violation[1]+wErr_aq_violation[1])

    # switch_points = get_data_from_path(wErr_controllers_path, retrieve_string)
    # print(wErr_controllers_switch)

    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Smart Home World')

    axs[0, 0].set_title("Heater error controller temperature")
    axs[0, 0].plot(hHerr_temp_data)
    axs[0, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[0, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[0, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[0, 1].set_title("Heater error controller air quality")
    axs[0, 1].plot(hHerr_aq_data, 'r')
    axs[0, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[0, 1].axhline(y = 0, color = 'k', linestyle = '--')

    axs[1, 0].set_title("Heater broken comfort controller temperature")
    axs[1, 0].plot(whErr_temp_data)
    axs[1, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[1, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[1, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[1, 1].set_title("Heater broken comfort controller air quality")
    axs[1, 1].plot(whErr_aq_data, 'r')
    axs[1, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[1, 1].axhline(y = 0, color = 'k', linestyle = '--')

    axs[2, 0].set_title("Heater broken eco controller temperature")
    axs[2, 0].plot(wErr_temp_data)
    axs[2, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[2, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[2, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[2, 1].set_title("Heater broken eco controller air quality")
    axs[2, 1].plot(wErr_aq_data, 'r')
    axs[2, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[2, 1].axhline(y = 0, color = 'k', linestyle = '--')



    plt.show()

if __name__ == "__main__":
    main()
