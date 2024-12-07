from utils.servo import *

class HexapodLegJoint:
    def __init__(self, ports, initial_angle=0, angle_offset=0):
        self.pwm = i2c[ports[0]]
        self.channel = ports[1]
        self.angle_offset = angle_offset
        self.set_angle(initial_angle)
        
    def set_angle(self, angle):
        angle = max(-90, min(90, angle))
        adjusted_angle = angle + self.angle_offset
        pulse = int(servoMid + (adjusted_angle / 90) * pulseInterval)
        self.pwm.setPWM(self.channel, 0, pulse)
        self.angle = angle
        
    def get_angle(self):
        return self.angle
    
    pwm : PWM = None
    angle_offset = 0
    angle = 0

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

class Hexapod:
    def __init__(self, left_front_leg, left_mid_leg, left_back_leg, right_front_leg, right_mid_leg, right_back_leg):
        self.left_front_leg = left_front_leg
        self.left_mid_leg = left_mid_leg
        self.left_back_leg = left_back_leg
        self.right_front_leg = right_front_leg
        self.right_mid_leg = right_mid_leg
        self.right_back_leg = right_back_leg
