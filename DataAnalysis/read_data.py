from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

plt.rcParams.update({'font.size': 15})
'''Remeber to modify the file first and add the experiment info
'''
def process_data(file_name, enable_data_desciption):
    '''
    If the first line of data.txt descibe the experiment condition, enable_data_description = True
    :return: calibrated_times, AC_inner, AC_outer
    '''
    AC_two_channel_file = open(file_name, 'r')


    #Code
    if enable_data_desciption:
        Lines = AC_two_channel_file.readlines()

    count = 0
    timestamps = []
    AC_inner = []
    AC_outer = []
    seconds_times = []
    calibrated_times = []

    # Strips the newline character
    for line in Lines[1:]:
        count += 1
        line_content = line.strip()
        if count % 3 == 1:
            timestamps.append(line_content)
        elif count % 3 == 2:
            AC_inner.append(float(line_content))
        elif count % 3 == 0:
            AC_outer.append(float(line_content))

    for time_str in timestamps:
        time_str = time_str.split(':')
        time_new = float(time_str[0])*60 + float(time_str[1])*60 + float(time_str[2])
        # print(time_new)
        seconds_times.append(time_new)
    start_time = seconds_times[0]

    calibrated_times = [(item - start_time)*100 for item in seconds_times]
    return calibrated_times, AC_inner, AC_outer



def get_average_potential_diff(calibrated_times, AC, cut_off_time, duration):
    useful_time = [x for x in calibrated_times if x <= cut_off_time]
    useful_index = len(useful_time) - 1
    useful_AC = AC[:useful_index]
    step = int(useful_index / duration)
    average_list = []
    for i, _ in enumerate(useful_AC[::step]):
        sub_list = useful_AC[i*step:] if (i+1)*step > len(useful_AC) else useful_AC[i*step:(i+1)*step]
        average_value = max(sub_list) - min(sub_list)
        average_list.append(average_value)
    return average_list


def get_average_potential_DC(calibrated_times, AC, cut_off_time, duration):
    useful_time = [x for x in calibrated_times if x <= cut_off_time]
    useful_index = len(useful_time) - 1
    useful_AC = AC[:useful_index]
    step = int(useful_index / duration)
    average_list = []
    for i, _ in enumerate(useful_AC[::step]):
        sub_list = useful_AC[i*step:] if (i+1)*step > len(useful_AC) else useful_AC[i*step:(i+1)*step]
        average_value = sum(sub_list)/len(sub_list)
        average_list.append(average_value)
    return average_list

def Average(lst):
    lst.remove(max(lst))
    lst.remove(min(lst))
    return sum(lst) / len(lst)

def plot_channel(calibrated_times, AC_channel1, AC_channel2):
    plt.plot(calibrated_times, AC_channel1, '.', linestyle='-', color='g', label = "Voltage between WE and CE")
    plt.plot(calibrated_times, AC_channel2, '.', linestyle='-', color='r', label = "Voltage between WSE and RE")
    plt.legend()
    plt.xlim((0,6000))
    plt.xlabel("Time [$10mS$]")
    plt.ylabel("Potential Difference [$V$]")
    plt.show()

def plot_channel_2(calibrated_times, AC_channel1, title = "x"):
    figure(figsize = (10, 6), dpi = 80)
    if calibrated_times[0] != 0:
        calibrated_times = [calibrated_time - calibrated_times[0] for calibrated_time in calibrated_times]
    plt.plot(calibrated_times, AC_channel1, '.', linestyle='-', color='b')
    plt.xlabel("Time [$10mS$]")
    plt.ylabel("Potential Difference [$V$]")
    plt.xlim(0,100)
    plt.title(title)
    plt.show()
