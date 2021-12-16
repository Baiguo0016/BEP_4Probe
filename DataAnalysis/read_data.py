from matplotlib import pyplot as plt

AC_two_channel_file = open('test_data.txt', 'r')
Lines = AC_two_channel_file.readlines()

count = 0
timestamps = []
AC_1channels = []
AC_2channels = []
seconds_times = []
calibrated_times = []
# Strips the newline character
for line in Lines:
    count += 1
    line_content = line.strip()
    if count % 3 == 1:
        timestamps.append(line_content)
    elif count % 3 == 2:
        AC_1channels.append(float(line_content))
    elif count % 3 == 0:
        AC_2channels.append(float(line_content))

for time_str in timestamps:
    time_str = time_str.split(':')
    time_new = float(time_str[0])*60 + float(time_str[1])*60 + float(time_str[2])
    # print(time_new)
    seconds_times.append(time_new)
start_time = seconds_times[0]

calibrated_times = [(item - start_time)*100 for item in seconds_times]

plt.plot(calibrated_times[0:100], AC_1channels[0:100], linestyle='--', marker='o', color='b', )
plt.show()
