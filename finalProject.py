import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(07, GPIO.IN)

#use pwm on inputs so motors don't go too fast
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

#make a global variable to communicate between sonar function and main loop
globalstop=0
finished = False
fast = 20
slow = 10

#assigning variable names to each sensor's pin
farLeft = 18
left = 13
middle = 11
right = 12
farRight = 7

def straight():
	'''goes straight'''
	#right wheel goes forward fast
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	#left wheel goes forward fast
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('follow line - straight')

def leanLeft():
	'''turns right since robot is leaning left to adjust itself back onto following the line'''
	#right wheel goes backwards fast
	p.ChangeDutyCycle(0)
	q.ChangeDutyCycle(fast)
	#left wheeel goes forward fast
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('follow line - leaned left so turned right')
	
def leanRight():
	'''turns left since robot is leaning right to adjust itself back onto following the line'''
	#right wheel goes forwards fast
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	#left wheel goes backwards fast
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(fast)
	print('follow line - leaned right so turned left')

def turnRight():
	'''turns right'''
	#the right wheel goes backwards slowly
	p.ChangeDutyCycle(0)
	q.ChangeDutyCycle(slow)
	#the left wheel goes forwards fast
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('right turn')
	#turns right for 0.5 seconds
	time.sleep(0.5)

def turnAround():
	'''turns around using a left turn'''
	#right wheel goes forwards fast
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	#left wheel goes backwards fast
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(fast)
	print('turn around')

def followLine():
	'''follows the line depending on the middle three sensors'''
	#if the middle sensor is on black, the robot goes straight
	if GPIO.input(middle)==1:
		straight()
	#if the left sensor is on black, the robot is leaning right, so it turns left
	elif GPIO.input(left)==1:
		leanRight()
	#if the right sensor is on black, the robot is leaning left, so it turns right
	elif GPIO.input(right)==1:
		leanLeft()

try:
       while True:
		  #prints what the line sensors are sensing 
		  print('far right = ' + str(GPIO.input(farRight)) + 'right = ' + str(GPIO.input(right)) + 'middle = ' + str(GPIO.input(middle)) + 'left = ' + str(GPIO.input(left)) + 'farLeft = ' + str(GPIO.input(farLeft)))
		  #when all the sensors are on white, this means the robot has hit a dead end, so it turns around
		  if GPIO.input(farLeft)==0 and GPIO.input(left)==0 and GPIO.input(middle)==0 and GPIO.input(right)==0 and GPIO.input(farRight)==0:
			  turnAround()
		  #if the far right and far left sensors are on white, then the robot follows the line because it should be on a straight line
		  elif GPIO.input(farLeft)==0 and GPIO.input(farRight)==0:
			  followLine()
		  #if the far right sensor is on black, there is a path to the right, so it turns right
		  elif GPIO.input(farRight)==1:
			  turnRight()
		  #if the left and middle sensors are on black, the robot goes straight so it will eventually get back on course 
		  elif GPIO.input(left)==1 and GPIO.input(middle)==1:	
			  straight()
		  #if the right and middle sensors are on black, the robot goes straight so it will eventualy get back on course
		  elif GPIO.input(right)==1 and GPIO.input(middle)==1:
			  straight()
		 	  
except KeyboardInterrupt:
       finished = True  # stop other loops
       GPIO.cleanup()
       sys.exit()

