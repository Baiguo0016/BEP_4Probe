import spidev
import RPi.GPIO as gpio
from datetime import datetime

SAVE = False

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(37, gpio.OUT, initial=1)
gpio.setup(33, gpio.OUT, initial=1)
gpio.output(37, 0)

spi = spidev.SpiDev()
spi.open(1,0)
spi.mode = 0b00
#The max sampling speed can be change probabily up to 7KHz, 60KHz for max_speed_hz
spi.max_speed_hz = 1000
spi.writebytes([0b01011000, 0b10101001, 0b00000000, 0b00001111, 0b00111111, 0b01000000, 0b01010000, 0b00000000, 0b00000000, 0b00000000])
gpio.output(37, 1)
gpio.output(37, 0)
spi.writebytes([0b01000001])

if SAVE:
	f = open("data.txt", "w")
else:
	maxIndex = 1000
	list1 = [0] * maxIndex
	list2 = [0] * maxIndex
	index = 0

while True:
	x =  spi.readbytes(3)
	v1 = spi.readbytes(3)
	x = spi.readbytes(3)
	v2 = spi.readbytes(3)
	if v1[0] & 0b10000000:
		v1 = [x ^ 0xFF for x in v1]
		data1 = float(-(v1[0]*65536+v1[1]*256+v1[2]+1))
	else:
		data1 = float(v1[0]*65536+v1[1]*256+v1[2])
	if v2[0] & 0b10000000:
		v2 = [x ^ 0xFF for x in v2]
		data2 = float(-(v2[0]*65536+v2[1]*256+v2[2]+1))
	else:
		data2 = float(v2[0]*65536+v2[1]*256+v2[2])

	voltage1 = data1
	voltage1 = data1/1.5/8388608/6.8*33
	voltage1 = voltage1*1.172947147-0.0028 #calibrate
	voltage2 = data2/1.5/8388608/6.8*33
	voltage2 = voltage2*1.172947147-0.0028

	if SAVE:
		f.write(datetime.now().strftime("%H:%M:%S.%f") + "\n")
		f.write(str(voltage1) + "\n")
		f.write(str(voltage2) + "\n")
	else:
		list1[index] = voltage1
		list2[index] = voltage2
		index += 1
		index %= maxIndex
		print("now_1={:0.8f}V, now_2={:0.8f}V, avg_1={:0.8f}V, avg_2={:0.8f}V".format(voltage1, voltage2, sum(list1)/maxIndex, sum(list2)/maxIndex), end="\r")
gpio.output(37, 1)
spi.close();
