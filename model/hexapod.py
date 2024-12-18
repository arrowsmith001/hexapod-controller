import math
from utils.servo import *
from config import *

class HexapodLegJoint:
    def __init__(self, ports, angle_offset=0, initial_angle=0, invert=False):
        self.pwm = i2c[ports[0]]
        self.channel = ports[1]
        self.invert = invert
        self.angle_offset = angle_offset
        self.initial_angle = initial_angle
    
    def set_to_initial_angle(self):
        self.set_angle(self.initial_angle)

    def set_angle(self, angle):
        self.angle = angle
        angle = -angle if self.invert else angle
        angle = max(-90, min(90, angle))
        adjusted_angle = angle + self.angle_offset
        pulse = int(servoMid + (adjusted_angle / 90) * pulseInterval)
        self.pwm.setPWM(self.channel, 0, pulse)
        
    def get_angle(self):
        return self.angle
    
    pwm : PWM = None
    angle_offset = 0
    angle = 0

def calculate_foot_rest_position(origin, heading):
    x = origin[0] + femur_len * math.cos(math.radians(heading))
    y = origin[1] + femur_len * math.sin(math.radians(heading))
    z = origin[2] - tibia_len
    return [x, y, z]

class HexapodLeg:
    def __init__(self, origin, heading, joint0, joint1, joint2):
        self.origin = origin
        self.heading = heading
        self.joints = [joint0, joint1, joint2]
        self.foot_rest_position = calculate_foot_rest_position(self.origin, self.heading)

    def set_initial_angles(self):
        for i in range(3):
            self.joints[i].set_to_initial_angle()
        
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
        if left_front_leg is not None: left_front_leg.set_initial_angles()
        if left_mid_leg is not None: left_mid_leg.set_initial_angles()
        if left_back_leg is not None: left_back_leg.set_initial_angles()
        if right_front_leg is not None: right_front_leg.set_initial_angles()
        if right_mid_leg is not None: right_mid_leg.set_initial_angles()
        if right_back_leg is not None: right_back_leg.set_initial_angles()
