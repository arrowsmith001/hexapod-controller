from lib.Adafruit_PWM_Servo_Driver import PWM

freq = 50
pulseInterval = 205
servoMin = 102  # 0 degrees
servoMid = servoMin + pulseInterval  # 90 degrees
servoMax = servoMid + pulseInterval  # 180 degrees

i2c = [PWM(0x40, debug=False), PWM(0x41, debug=False)]

i2c[0].setPWMFreq(freq)
i2c[1].setPWMFreq(freq)    

def kill_servos():
    for i in range(16):
        i2c[0].setPWM(i, 0, 0)
        i2c[1].setPWM(i, 0, 0)

# TODO: Test if this makes a difference
# def setServoPulse(channel, pulse):
#   pulseLength = 1000000                   
#   pulseLength /= 50                       
#   print ("%d us per period" % pulseLength)
#   pulseLength /= 4096                     
#   print ("%d us per bit" % pulseLength)
#   pulse *= 1000
#   pulse /= pulseLength
#   pwm0.setPWM(channel, 0, pulse)
#   pwm1.setPWM(channel, 0, pulse)

# setServoPulse(0, 1500)
# setServoPulse(1, 1500)
# setServoPulse(2, 1500)