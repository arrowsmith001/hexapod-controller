from lib.Adafruit_PWM_Servo_Driver import PWM
from servo_drivers.abstract import ServoDriver

# I use a 32-channel Pi Hat which uses 2 different I2C addresses each with up to 16 PWM channels: 
#   - 0-1 for the PWM channel
#   - 0-15 for the port number

freq = 50
pulseInterval = 205
servoMin = 102  # 0 degrees
servoMid = servoMin + pulseInterval  # 90 degrees
servoMax = servoMid + pulseInterval  # 180 degrees

class PiHatPWMDriver(ServoDriver):
    
    def __init__(self):
        self.i2c: list[PWM] = [PWM(0x40, debug=False), PWM(0x41, debug=False)]
        self.i2c[0].setPWMFreq(freq)
        self.i2c[1].setPWMFreq(freq)

    def set_angle(self, address: list[int], angle: float):
        pulse = int(servoMid + (angle / 90) * pulseInterval)
        pwm = self.i2c[address[0]]
        channel = address[1]
        pwm.setPWM(channel, 0, pulse)
    
    def kill(self):
        for i in range(16):
            self.i2c[0].setPWM(i, 0, 0)
            self.i2c[1].setPWM(i, 0, 0)