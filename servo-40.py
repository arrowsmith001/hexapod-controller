#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)
 #  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  pwm.setPWM(0, 0, servoMin)
  pwm.setPWM(1, 0, servoMin)
  pwm.setPWM(2, 0, servoMin) 
  pwm.setPWM(3, 0, servoMin)
  pwm.setPWM(4, 0, servoMin) 
  pwm.setPWM(5, 0, servoMin)
  pwm.setPWM(6, 0, servoMin)
  pwm.setPWM(7, 0, servoMin) 
  pwm.setPWM(8, 0, servoMin)
  pwm.setPWM(9, 0, servoMin) 
  pwm.setPWM(10, 0, servoMin)
  pwm.setPWM(11, 0, servoMin)
  pwm.setPWM(12, 0, servoMin) 
  pwm.setPWM(13, 0, servoMin)
  pwm.setPWM(14, 0, servoMin) 
  pwm.setPWM(15, 0, servoMin)
  time.sleep(1)
  pwm.setPWM(0, 0, servoMax)
  pwm.setPWM(1, 0, servoMax)
  pwm.setPWM(2, 0, servoMax)
  pwm.setPWM(3, 0, servoMax)
  pwm.setPWM(4, 0, servoMax)
  pwm.setPWM(5, 0, servoMax) 
  pwm.setPWM(6, 0, servoMax)
  pwm.setPWM(7, 0, servoMax)
  pwm.setPWM(8, 0, servoMax)
  pwm.setPWM(9, 0, servoMax)
  pwm.setPWM(10, 0, servoMax)
  pwm.setPWM(11, 0, servoMax)
  pwm.setPWM(12, 0, servoMax)
  pwm.setPWM(13, 0, servoMax)
  pwm.setPWM(14, 0, servoMax)
  pwm.setPWM(15, 0, servoMax)
  time.sleep(1)




