from servo_drivers.abstract import ServoDriver
import math
from enum import Enum
from leg_position import LegPosition
from motion import Gait, Motion
from servo_drivers.abstract import ServoDriver
from utils.servo import *
from constants import *
    

class HexapodLegJoint:
    def __init__(self, driver: ServoDriver, address, angle_offset=0, initial_angle=0, invert=False):
        self.driver = driver
        self.address = address
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
        self.driver.set_angle(self.address, adjusted_angle)
        
    def get_angle(self):
        return self.angle
    
    # For fine-tuning the resting angle
    angle_offset = 0
    angle = 0
