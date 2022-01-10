from read_data import *

file_name = 'Date_12_21\\test_data_DC.txt'
calibrated_times, AC_inner, AC_outer = process_data(file_name, True)
plt_title = "(b)"
plot_channel_2(calibrated_times[:], AC_outer[:], title = plt_title)
