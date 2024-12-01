#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================

# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x41, debug=True)

servoMin = 102  # Min pulse length out of 4096 (1 ms)
servoMid = 307  # Mid pulse length out of 4096 (1.5 ms)
servoMax = 512  # Max pulse length out of 4096 (2 ms)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 50 Hz
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(50)                        # Set frequency to 50 Hz
while (True):
  # Change speed of continuous servo on channel 0
  pwm.setPWM(15, 0, servoMin)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMid)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMax)
  time.sleep(0.5)
  pwm.setPWM(15, 0, servoMid)
  time.sleep(0.5)
