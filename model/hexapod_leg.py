import math
import numpy as np
from enum import Enum
from hexapod.leg_position import LegType
from hexapod.motion import Gait, Motion
from hexapod.constants import *
from model.hexapod_leg_joint import HexapodLegJoint
from servo_drivers.abstract import ServoDriver
from utils.servo import *
from utils.ik import trajectory_as_angles, leg_ik
    

from model.hexapod_leg_joint import HexapodLegJoint


class HexapodLeg:
    def __init__(self, origin, starting_position, hip_joint : HexapodLegJoint, knee_joint : HexapodLegJoint, ankle_joint : HexapodLegJoint, joint_rest_headings):
        self.origin = np.array(origin)
        self.joints = [hip_joint, knee_joint, ankle_joint]
        self.joint_rest_headings = joint_rest_headings
        self.leg_heading = joint_rest_headings[0]
        self.femur_rest_angle = joint_rest_headings[1]
        self.tibia_rest_angle = joint_rest_headings[2]
        self.starting_position = np.array(starting_position)
        self.starting_angles = leg_ik(starting_position - self.origin, joint_rest_headings)
        print('Starting angles for leg at {origin}: {angles}'.format(origin=origin, angles=self.starting_angles))
        self.set_angles(self.starting_angles)
    

    def set_angles_to_zero(self):
        for i in range(3):
            self.joints[i].set_angle_to_zero()
        
    def set_angles(self, angles: np.ndarray):
        for i in range(3):
            self.joints[i].set_angle(angles[i])
        
    def get_angles(self):
        angles: list[float] = []
        for i in range(3):
            angles.append(self.joints[i].get_angle())
        return angles
    
    def get_initial_foot_position(self):
        return self.get_foot_position_at_angles(np.zeros(3, dtype=float))
    
    def get_foot_position(self):
        theta_0 = math.radians(self.joints[0].get_angle())
        theta_1 = math.radians(self.joints[1].get_angle())
        theta_2 = math.radians(self.joints[2].get_angle())
        return self.get_foot_position_at_angles(np.array([theta_0, theta_1, theta_2]))
    
    def get_foot_position_at_angles(self, angles: np.ndarray):
        theta_0 = np.deg2rad(angles[0])
        theta_1 = np.deg2rad(angles[1])
        theta_2 = np.deg2rad(angles[2])
        
        coxa_rest = np.deg2rad(self.leg_heading)
        femur_rest = np.deg2rad(self.femur_rest_angle)
        tibia_rest = np.deg2rad(self.tibia_rest_angle)
        
        outward = coxa_len + femur_len * math.cos(femur_rest + theta_1) + tibia_len * math.cos(femur_rest + tibia_rest + theta_1 + theta_2)
        x = self.origin[0] + outward * math.sin(theta_0 + coxa_rest)
        y = self.origin[1] + outward * math.cos(theta_0 + coxa_rest)
        z = self.origin[2] + coxa_elevation - femur_len * math.sin(femur_rest + theta_1) - tibia_len * math.sin(femur_rest + tibia_rest + theta_1 + theta_2)
        
        return np.array([x, y, z], dtype=float)
        
    
    def print_foot_position(self, label):
        pos = self.get_foot_position()
        print(label + ': ' + str(pos[0]) + ', ' + str(pos[1]) + ', ' + str(pos[2]))

