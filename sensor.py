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
spi.max_speed_hz = 1000
spi.writebytes([0b01011000, 0b00101001, 0b00000000, 0b00001111, 0b00111111, 0b01000000, 0b01010000, 0b00000000, 0b00000000, 0b00000000])
gpio.output(37, 1)
gpio.output(37, 0)
spi.writebytes([0b01000111])

if SAVE:
	f = open("data.txt", "w")
else:
	maxIndex = 1000
	list = [0] * maxIndex
	index = 0

while True:
	v = spi.readbytes(3)
	if v[0] & 0b10000000:
		v = [x ^ 0xFF for x in v]
		data = float(-(v[0]*65536+v[1]*256+v[2]+1))
	else:
		data = float(v[0]*65536+v[1]*256+v[2])
	voltage = data/1.5/8388608/6.8*33
	voltage = voltage*1.172947147-0.0028
	if SAVE:
		#f.write(datetime.now().strftime("%H:%M:%S.%f") + "\n")
		f.write(str(voltage) + "\n")
	else:
		list[index] = voltage
		index += 1
		index %= maxIndex
		print("now={:0.8f}V, max={:0.8f}V, min={:0.8f}V, avg={:0.8f}".format(voltage, max(list), min(list), sum(list)/maxIndex), end="\r")
gpio.output(37, 1)
spi.close();
