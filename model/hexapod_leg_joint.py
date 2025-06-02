from servo_drivers.abstract import ServoDriver
import math
from enum import Enum
from hexapod.leg_position import LegType
from hexapod.motion import Gait, Motion
from hexapod.constants import *
from servo_drivers.abstract import ServoDriver
from utils.servo import *
    

class HexapodLegJoint:
    def __init__(self, driver: ServoDriver, address, angle_nudge=0, invert=False):
        self.driver = driver
        self.address = address
        self.invert = invert
        self.angle_nudge = angle_nudge
    
    def set_angle_to_zero(self):
        self.set_angle(0)

    def set_angle(self, angle):
        self.angle = angle
        angle = -angle if self.invert else angle
        angle = max(-90, min(90, angle))
        adjusted_angle = angle + self.angle_nudge
        #print(f"Setting angle for joint {self.address} to {adjusted_angle} (original: {angle}, nudge: {self.angle_nudge})")
        self.driver.set_angle(self.address, adjusted_angle)
        
    def get_angle(self):
        return self.angle
    
    # For fine-tuning the resting angle
    angle_nudge = 0
    angle = 0
