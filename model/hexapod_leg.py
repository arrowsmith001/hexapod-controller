import math
import numpy as np
from enum import Enum
from leg_position import LegPosition
from model.hexapod_leg_joint import HexapodLegJoint
from motion import Gait, Motion
from servo_drivers.abstract import ServoDriver
from utils.servo import *
from constants import *
from utils.ik import trajectory_as_angles
    

from model.hexapod_leg_joint import HexapodLegJoint


class HexapodLeg:
    def __init__(self, origin, heading, joint0 : HexapodLegJoint, joint1 : HexapodLegJoint, joint2 : HexapodLegJoint):
        self.origin = origin
        self.heading = heading
        self.joints = [joint0, joint1, joint2]
        self.foot_start_position = self.get_foot_position()

    def set_initial_angles(self):
        for i in range(3):
            self.joints[i].set_to_initial_angle()
        
    def set_angles(self, angles: np.ndarray):
        for i in range(3):
            self.joints[i].set_angle(angles[i])
        
    def get_angles(self):
        angles: list[float] = []
        for i in range(3):
            angles.append(self.joints[i].get_angle())
        return angles
    
    def get_foot_position(self):
        theta_0 = math.radians(self.joints[0].get_angle())
        theta_1 = math.radians(self.joints[1].get_angle())
        theta_2 = math.radians(self.joints[2].get_angle())
        
        outward = coxa_len + femur_len * math.cos(math.radians(15 + theta_1)) + tibia_len * math.cos(math.radians(15 + 49 + theta_1 + theta_2))
        x = self.origin[0] + outward * math.sin(theta_0 - math.radians(self.heading) - math.pi)
        y = self.origin[1] + outward * math.cos(theta_0 - math.radians(self.heading))

        def get_motion_count(self, leg):
            raise NotImplementedError

        z = self.origin[2] + coxa_elevation - femur_len * math.sin(math.radians(14.795 + theta_1)) - tibia_len * math.sin(math.radians(14.795 + 49.168 + theta_1 + theta_2))
        
        return [x, y, z]
    
    def print_foot_position(self, label):
        pos = self.get_foot_position()
        print(label + ': ' + str(pos[0]) + ', ' + str(pos[1]) + ', ' + str(pos[2]))

