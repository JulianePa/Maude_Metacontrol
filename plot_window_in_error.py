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
    wHerr_temp_path = 'WErrTempLog.txt'
    wHerr_aq_path = 'WErrAirqualityLog.txt'

    comf_temp_path = 'WBrokenComfTempLog.txt'
    comf_aq_path = 'WBrokenComfAirqualityLog.txt'

    eco_temp_path = 'WBrokenEcoTempLog.txt'
    eco_aq_path = 'WBrokenEcoAirqualityLog.txt'


    wHerr_temp_data = get_data_from_path(wHerr_temp_path)
    wHerr_aq_data = get_data_from_path(wHerr_aq_path)
    wHerr_temp_violation = calculate_violations(wHerr_temp_data, 'temp')
    wHerr_aq_violation = calculate_violations(wHerr_aq_data, 'aq')
    print('WindowErr number temp violation: ',wHerr_temp_violation[0], ' number AQ violation: ',wHerr_aq_violation[0], ' total number of violation: ', wHerr_temp_violation[0]+wHerr_aq_violation[0])
    print('WindowErr amount temp violation: ',wHerr_temp_violation[1], ' amount AQ violation: ',wHerr_aq_violation[1], ' total amount of violation: ', wHerr_temp_violation[1]+wHerr_aq_violation[1])
    print('-------------')

    comf_temp_data = get_data_from_path(comf_temp_path)
    comf_aq_data = get_data_from_path(comf_aq_path)
    comf_temp_violation = calculate_violations(comf_temp_data, 'temp')
    comf_aq_violation = calculate_violations(comf_aq_data, 'aq')
    print('Comfort temp number violation: ',comf_temp_violation[0], ' number AQ violation: ',comf_aq_violation[0], ' total number of violation: ', comf_temp_violation[0]+comf_aq_violation[0])
    print('Comfort temp amount violation: ',comf_temp_violation[1], ' amount AQ violation: ',comf_aq_violation[1], ' total amount of violation: ', comf_temp_violation[1]+comf_aq_violation[1])
    print('-------------')

    eco_temp_data = get_data_from_path(eco_temp_path)
    eco_aq_data = get_data_from_path(eco_aq_path)
    eco_temp_violation = calculate_violations(eco_temp_data, 'temp')
    eco_aq_violation = calculate_violations(eco_aq_data, 'aq')
    print('Eco number temp violation: ',eco_temp_violation[0], ' number AQ violation: ',eco_aq_violation[0], ' total number of violation: ', eco_temp_violation[0]+eco_aq_violation[0])
    print('Eco amount temp violation: ',eco_temp_violation[1], ' amount AQ violation: ',eco_aq_violation[1], ' total amount of violation: ', eco_temp_violation[1]+eco_aq_violation[1])

    # switch_points = get_data_from_path(eco_controllers_path, retrieve_string)
    # print(eco_controllers_switch)

    fig, axs = plt.subplots(3, 2)
    fig.suptitle('Smart Home World')

    axs[0, 0].set_title("Window error controller temperature")
    axs[0, 0].plot(wHerr_temp_data)
    axs[0, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[0, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[0, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[0, 1].set_title("Window error controller air quality")
    axs[0, 1].plot(wHerr_aq_data, 'r')
    axs[0, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[0, 1].axhline(y = 0, color = 'k', linestyle = '--')

    axs[1, 0].set_title("Window broken comfort controller temperature")
    axs[1, 0].plot(comf_temp_data)
    axs[1, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[1, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[1, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[1, 1].set_title("Window broken comfort controller air quality")
    axs[1, 1].plot(comf_aq_data, 'r')
    axs[1, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[1, 1].axhline(y = 0, color = 'k', linestyle = '--')

    axs[2, 0].set_title("Window broken eco controller temperature")
    axs[2, 0].plot(eco_temp_data)
    axs[2, 0].set(xlabel='Time step', ylabel='Temperature')
    axs[2, 0].axhline(y = 18, color = 'k', linestyle = '--')
    axs[2, 0].axhline(y = 22, color = 'k', linestyle = '--')

    axs[2, 1].set_title("Window broken eco controller air quality")
    axs[2, 1].plot(eco_aq_data, 'r')
    axs[2, 1].set(xlabel='Time step', ylabel='Air quality')
    axs[2, 1].axhline(y = 0, color = 'k', linestyle = '--')



    plt.show()

if __name__ == "__main__":
    main()
