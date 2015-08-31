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

#assigning variable names
farLeft = 18
left = 13
middle = 11
right = 12
farRight = 7

def straight():
	#goes straight
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('straight')

def leanLeft():
	#turns right since robot is leaning left
	p.ChangeDutyCycle(0)
	q.ChangeDutyCycle(fast)
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('leaned left so turned right')
	
def leanRight():
	#turns left since robot is leaning right
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(fast)
	print('leaned right so turned left')

def turnRight():
	#turns right
	p.ChangeDutyCycle(0)
	q.ChangeDutyCycle(slow)
	a.ChangeDutyCycle(fast)
	b.ChangeDutyCycle(0)
	print('right turn')
	time.sleep(0.5)

def turnLeft():
	#turns left
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(slow)
	print('left turn')
	time.sleep(0.5)
	
def turnAround():
	#turns around 180 degrees using a left turn
	p.ChangeDutyCycle(fast)
	q.ChangeDutyCycle(0)
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(0)
	print('turn around')
	time.sleep(0.5)

def stop():
	p.ChangeDutyCycle(0)
	q.ChangeDutyCycle(0)
	a.ChangeDutyCycle(0)
	b.ChangeDutyCycle(0)
	print('stop')

def followLine():
	if GPIO.input(left)==0 and GPIO.input(right)==0:
		straight()
	if GPIO.input(left)==1:
		leanRight()
	if GPIO.input(right)==1:
		leanLeft()

try:
       while True:
#                  if GPIO.input(12)==1 and GPIO.input(13)==1 or globalstop==1:
#                  if False:
#                          a.ChangeDutyCycle(0)
#                          b.ChangeDutyCycle(0)
#                          p.ChangeDutyCycle(0)
#                          q.ChangeDutyCycle(0)
#                          time.sleep(0.5)
#                          print('stop')
		  if GPIO.input(farLeft)==0 and GPIO.input(farRight)==0:
			  followLine()
		  elif GPIO.input(farLeft)==0 and GPIO.input(farRight)==1:
			  turnRight()
		  elif GPIO.input(farLeft)==1 and GPIO.input(farRight)==0:
			  turnLeft()
		  elif GPIO.input(farLeft)==1 and GPIO.input(farRight)==1:
			  turnRight()
	  
except KeyboardInterrupt:
       finished = True  # stop other loops
       GPIO.cleanup()
       sys.exit()
