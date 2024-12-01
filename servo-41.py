#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time


pwm = PWM(0x41, debug=True) # Toggle between 0x40 and 0x41 for U2 and U3

servoMin = 102  # 0 degrees
servoMid = 307  # 90 degrees
servoMax = 512  # 180 degrees

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   
  pulseLength /= 50                       
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(50)                        
while (True):
  pwm.setPWM(15, 0, servoMin)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMid)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMax)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMid)
  time.sleep(0.5)
