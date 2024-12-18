from model.hexapod import *
from utils.move import *
from utils.servo import *
from config import *
import math
import numpy as np

def get_rot_mat_2d(angle):
    angle = angle * (math.pi / 180)  # Convert to radians
    return np.array([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])

def get_rot_mat_3d(angle):
    angle = angle * (math.pi / 180)  # Convert to radians
    return np.array([[math.cos(angle), math.sin(angle),0], [-math.sin(angle), math.cos(angle),0], [0,0,1]])

def cosine_rule_from_sides(adjacent_sides, opposite_side):
    a, b = adjacent_sides
    c = opposite_side
    return math.acos((a**2 + b**2 - c**2) / (2 * a * b))

# Given a start and end point in 3D space, for each point between them calculate the required 
#   angles to reach that point, and return as an array
def trajectory_as_angles(start, end, steps, leg_rest_heading):
    trajectory = []
    for i in range(steps):
        target = start + (i / steps) * (end - start)
        angles = leg_ik(target, leg_rest_heading)
        trajectory.append(angles)
    return trajectory

# Given a target position in world space, and the rest heading of the leg, calculate the angles 
#   required to reach that position
def leg_ik(target_pos, leg_rest_heading):
    
    # Normalize target position to leg space by removing the leg rest heading
    targ_norm_1 = get_rot_mat_3d(-leg_rest_heading).dot(target_pos)
    
    theta_0 = math.atan2(targ_norm_1[0], targ_norm_1[1])
    
    # Normalize target position again by removing the theta_0 angle.
    # This allows us to work with the remaining joints in the y-z plane.
    targ_norm_2 = get_rot_mat_3d(-rad2deg(theta_0)).dot(targ_norm_1)
    
    # Calculate the distance from the end of the coxa to the target position
    d_vec = targ_norm_2 - np.array([0, coxa_len, coxa_elevation]) # Remove coxa offset from hip
    d = np.linalg.norm(d_vec)
    
    j1_rest_heading = 15 # in y-z plane TODO: Should be refactored to leg config
    j2_rest_heading = 49 # in y-z plane TODO: Should be refactored to leg config

    # If target is unreachable, just move the leg as far as possible pointed at target
    if(d > femur_len + tibia_len):
        theta_1 = math.atan2(-d_vec[2], d_vec[1]) - np.deg2rad(j1_rest_heading)
        theta_2 = -np.deg2rad(j2_rest_heading)
    else:
        beta = cosine_rule_from_sides([femur_len, tibia_len], d)
        alpha = cosine_rule_from_sides([femur_len, d], tibia_len)
        descent_angle = math.atan2(-d_vec[2], d_vec[1]) - np.deg2rad(j1_rest_heading)
        theta_1 = descent_angle - alpha
        theta_2 = math.pi - beta - np.deg2rad(j2_rest_heading)
    
    theta_0 = clamp_angle(-100, 100, np.rad2deg(theta_0))
    theta_1 = clamp_angle(-100, 100, np.rad2deg(theta_1))
    theta_2 = clamp_angle(-100, 100, np.rad2deg(theta_2))

    return [theta_0, theta_1, theta_2]


def clamp_angle(lower, upper, angle):
    while angle < lower or angle > upper:
        if angle < lower:
            angle += 360
        if angle > upper:
            angle -= 360
    return angle