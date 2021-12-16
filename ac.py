import spidev
import RPi.GPIO as gpio
from datetime import datetime, timedelta
import math

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(13, gpio.OUT, initial=1)

done = False

while not done:
	spi = spidev.SpiDev()
	spi.open(0, 0)
	spi.mode = 0b00
	spi.max_speed_hz = 150000
	freq = float(input("Hz?"))
	amplitude = float(input("A?"))
	start = datetime.now()
	end = start + timedelta(minutes = 120)

	now = datetime.now()
	while now < end:
		delta = now - start
		current = amplitude*math.sin(2*math.pi*freq*delta.total_seconds())
		current += 5
		current /= 10
		current *= 1024
		current = int(current)
		#if current > 1023:
		#	current = 1023
		#elif current < 0:
		#	current = 0
		gpio.output(13, 0)
		command = list(current.to_bytes(2, byteorder="big"))
		msg = spi.xfer(command)
		gpio.output(13, 1)
		now = datetime.now()
spi.close();
