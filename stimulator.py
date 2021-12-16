import spidev
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(13, gpio.OUT, initial=1)

while True:
	current = input("A?")
	current = float(current);
	current *= 0.98119
	current += 0.03
	current += 5
	current /= 10
	current *= 1024
	current = int(current)
	print(current)
	command = list(current.to_bytes(2, byteorder="big"))
	print(command)
	spi = spidev.SpiDev()
	spi.open(0, 0)
	spi.mode = 0b00
	spi.max_speed_hz = 7692
	maxIndex = 100
	list = [0] * maxIndex
	index = 0
	while True:
		gpio.output(13, 0)
		to_send = command.copy()
		spi.xfer(to_send)
		msg = to_send
		adc = msg[1]*256 + msg[0]
		list[index] = adc
		index += 1
		index %= maxIndex
		print("now={0:04d}, max={1:04d}, min={2:04d}, avg={3:04d}".format(adc, max(list), min(list), int(sum(list)/maxIndex)), end="\r")
		gpio.output(13, 1)
		#time.sleep(1)

spi.close();
