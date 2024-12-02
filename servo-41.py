#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import math


pwm0 = PWM(0x40, debug=False)
pwm1 = PWM(0x41, debug=False)

pwm0.setPWMFreq(50)
pwm1.setPWMFreq(50)    

pulseInterval = 205
servoMin = 102  # 0 degrees
servoMid = servoMin + pulseInterval  # 90 degrees
servoMax = servoMid + pulseInterval  # 180 degrees

class HexapodLegJoint:
    def __init__(self, pwm: PWM, channel, angle=0):
        self.pwm = pwm
        self.channel = channel
        self.angle = 0
        self.set_angle(angle)
        
    def set_angle(self, angle):
        self.angle = angle
        pulse = int(servoMid + (angle / 90) * pulseInterval)
        self.pwm.setPWM(self.channel, 0, pulse)
        
    def get_angle(self):
        return self.angle

class HexapodLeg:
    def __init__(self, joint0, joint1, joint2):
        self.joints = [joint0, joint1, joint2]
        
    def set_angles(self, angles):
        for i in range(3):
            self.joints[i].set_angle(angles[i])
        
    def get_angles(self):
        angles = []
        for i in range(3):
            angles.append(self.joints[i].get_angle())
        return angles
    
    joints = []

class HexapodLegIK:
    def __init__(self, leg: HexapodLeg):
        self.leg = leg
        self.angles = [0, 0, 0]
        
    def set_position(self, x, y, z):
        self.angles = self.calculate_angles(x, y, z)
        self.leg.set_angles(self.angles)

    def calculate_angles(self, x, y, z):
        return [0, 0, 0]
    

right_mid_j0 = HexapodLegJoint(pwm0, 0, 0)
right_mid_j1 = HexapodLegJoint(pwm0, 1, 0)
right_mid_j2 = HexapodLegJoint(pwm0, 2, 0)

right_mid_leg = HexapodLeg(right_mid_j0, right_mid_j1, right_mid_j2)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   
  pulseLength /= 50                       
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm0.setPWM(channel, 0, pulse)
  pwm1.setPWM(channel, 0, pulse)

setServoPulse(0, 1500)
setServoPulse(1, 1500)
setServoPulse(2, 1500)

def move_joint(joint : HexapodLegJoint, target_angle, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angle = joint.get_angle()
    angle_step = (target_angle - start_angle) / steps
    for i in range(steps):
        joint.set_angle(start_angle + i * angle_step)
        time.sleep(dt)

def move_joints(joints, target_angles, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angles = [j.get_angle() for j in joints]
    angle_steps = [(target_angles[i] - start_angles[i]) / steps for i in range(len(joints))]
    for i in range(steps):
        for j in range(len(joints)):
            joints[j].set_angle(start_angles[j] + i * angle_steps[j])
        time.sleep(dt)

while True:
    move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [-45, -45, -45], 0.5) # fwd, up, up
    move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [45, -90, -45], 0.5)
    move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [0, 0, 0],  0.5)

# targ = [49.359, 1.496, -21.97]
  

# femur_len = 48.325
# # Right leg config
# theta0 = math.atan(targ[1]/targ[0])
# theta1 = 