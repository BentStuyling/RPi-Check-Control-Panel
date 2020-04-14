'''
Control the Brightness of LED using PWM on Raspberry Pi
http://www.electronicwings.com
'''

import RPi.GPIO as GPIO
from time import sleep
freq =60
dutycycle = 100

pin = 33				# PWM pin 
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(pin,GPIO.OUT)
pi_pwm = GPIO.PWM(pin,freq)		#create PWM instance with frequency
pi_pwm.start(dutycycle)

pulsewidth = round((1/freq)*(dutycycle/100)*1000,3)
print(pulsewidth,'ms')

sleep(10)
		#start PWM of required Duty Cycle
# while True:
#     for duty in range(0,101,1):
#         pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
#         sleep(0.1)

#     for duty in range(100,-1,-1):
#         pi_pwm.ChangeDutyCycle(duty)
#         sleep(0.1)

#     for freq in range(1,200,1):
#         pi_pwm.ChangeFrequency(freq)
#         sleep(0.1)
    
#     for freq in range(199,1,-1):
#         pi_pwm.ChangeFrequency(freq)
#         sleep(0.1)

#     sleep(0.5)