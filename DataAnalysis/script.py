from read_data import *


# '''
# For sample3_data_3, the last few seconds should be discard, because the protection resistor added.
# '''
# file_name = 'Sample3/AC_sample3_data_7.txt'
# calibrated_times, AC_inner, AC_outer = process_data(file_name, True)
# plot_channel(calibrated_times[0:], AC_outer[0:], AC_inner[0:])

#
# file_name = 'Date_12_20/Sample2/f50A1.txt'
# calibrated_times, AC_inner, AC_outer = process_data(file_name, True)
# end_index = 400
# plot_channel(calibrated_times, AC_outer, AC_inner)

# file_name = 'Sample3\AC_sample3_data_6.txt'
# calibrated_times, AC_inner, AC_outer = process_data(file_name, True)
# plot_channel(calibrated_times[0:], AC_outer[0:], AC_inner[0:])

#
# file_name = 'Date_12_20/Sample2/f100A1.txt'
# file_name = 'Date_12_23/pins_5/Sample_2/f10I1.txt'
file_name = 'Date_12_23/pins_5/Phantom_2/DC3mA.txt'
calibrated_times, AC_inner, AC_outer = process_data(file_name, True)
plot_channel(calibrated_times[:], AC_outer[:], AC_inner[:])

print("inner")
print(Average(get_average_potential_DC(calibrated_times[:], AC_inner[:], 100000, 100)))
# print(Average(get_average_potential_diff(calibrated_times[:], AC_inner[:], 100000, 100)))

print("outer")
print(Average(get_average_potential_DC(calibrated_times[:], AC_outer[:], 100000, 100)))
# print(Average(get_average_potential_diff(calibrated_times[:], AC_outer[:], 100000, 100)))

# print(Average(get_average_potential_diff(calibrated_times, AC_outer, 10000, 100)))
