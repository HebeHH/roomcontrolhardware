import RPi.GPIO as GPIO
import time

# server GPIOs: fan = 3, lights = 18, 7 

fan = False
aircon = False
temp = 0

fan_pin = 3
light_on_pin = 7
light_off_pin = 18

def reset_all():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)
	return None

def setup_servo(pin_num):
	GPIO.setup(pin_num, GPIO.OUT)
	p1 = GPIO.PWM(pin_num, 50)
	return p1

def move_servo(pin_num, pos):
	GPIO.setmode(GPIO.BOARD)
	p1 = setup_servo(pin_num)
	p1.start(pos)
	time.sleep(0.5)
	p1.stop()
	GPIO.cleanup()
	return None

# input = {0, 1, 2, 3, 4, 5} where 0 = off
def set_wind(val):
	val = int(val)
	pos = [2.5, 4.5, 6.5, 8.5, 10.5, 12.5]
	global fan
	if fan == True:
		move_servo(fan_pin, pos[val])
		print "adjusted"
	else:
		print "please turn on to adjust"
	return None

# input = {On, Off}
def set_fan(val):
	global fan
	if val == "On":
		fan = True
		move_servo(fan_pin, 9)
		print "turned on"
	else:
		fan = False
		move_servo(fan_pin, 2.3)
		print "turned off"
	return None

# input = {On, Off}
def set_lights(val):
	if val == "On":
		move_servo(light_on_pin, 3)
		print "turned on"
	else:
		move_servo(light_off_pin, 12)
		print "turned off"
	time.sleep(1)
	move_servo(light_on_pin, 8)
	move_servo(light_off_pin, 8)
	return None

# input = {On, Off}
def set_aircon(val):
	global aircon
	if val == "On":
		print "turned on"
		val = True
	else:
		print "turned off"
		val = False

	if val != aircon:
		print "changed"
		# TO DO: 
		# (requires hardware config)
		# press power button
		# wait a sec
	
	aircon = val
	return None

# input = integer 1-16ish
def set_temp(val):
	val = int(val)
	global temp
	change = val-temp
	if change == 0:
		"no change"
	elif change < 0:
		for i in range(-change):
			print "decreasing.."
			# TO DO:
			# push down button
			# hold
			# release
			# pause
		print "decreased"
	else:
		for i in range(change):
			print "increasing..."
			# TO DO:
			# push up button
			# hold
			# release
			# pause
		print "increased"

	temp = val
	return None

# needed to make sure of starting position for temp
def bottom_out_temp():
	for i in range(20):
		print "decreasing"
		# TO DO:
		# push down button
		# hold
		# release
		# pause
	print "temp decreased as much as possible"
	global temp
	temp = 0
	return None

