from utils.move import *
from utils.servo import *
from hexapod.constants import *
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
    arg = (a**2 + b**2 - c**2) / (2 * a * b)
    arg = max(-1, min(1, arg))
    return math.acos(arg)

# Given a start and end point in 3D space, for each point between them calculate the required 
#   angles to reach that point, and return as an array
def trajectory_as_angles(start, end, steps, rest_headings, control_point=None):
    trajectory = np.empty((steps, 3), dtype=float)
    start = np.array(start)
    end = np.array(end)
    if control_point is not None:
        control_point = np.array(control_point)
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        if control_point is not None:
            # Quadratic Bezier
            target = ((1 - t) ** 2) * start + (2 * (1 - t) * t) * control_point + (t ** 2) * end
        else:
            # Linear interpolation
            target = start + t * (end - start)
        angles = leg_ik(target, rest_headings)
        trajectory[i] = angles
    return trajectory

# Given a target position in local leg space, and the rest headings of the leg joints, calculate the angles required to reach that position
def leg_ik(target_pos, rest_headings):
    
    # print('Target position:', target_pos)
    
    # Unpack the rest headings
    leg_rest_heading = rest_headings[0]
    femur_rest_heading = rest_headings[1]
    tibia_rest_heading = rest_headings[2]
    
    # Normalize target position to leg space by removing the leg rest heading
    targ_norm_1 = get_rot_mat_3d(-leg_rest_heading).dot(target_pos)   
    
    theta_0 = -math.atan2(-targ_norm_1[0], targ_norm_1[1])
    
    # Normalize target position again by removing the theta_0 angle.
    # This allows us to work with the remaining joints in the y-z plane.
    # targ_norm_2[0] should always be 0 or very close to 0.
    targ_norm_2 = get_rot_mat_3d(rad2deg(-theta_0)).dot(targ_norm_1)
    
    # Calculate the distance from the end of the coxa to the target position
    # Remove coxa offset from hip. Now we are only dealing with the femur and tibia.
    d_vec = targ_norm_2 - np.array([0, coxa_len, coxa_elevation]) 
    d = np.linalg.norm(d_vec)
    
    # If target is unreachable, just move the leg as far as possible pointed at target
    if(d > femur_len + tibia_len):
        theta_1 = math.atan2(-d_vec[2], d_vec[1]) - np.deg2rad(femur_rest_heading)
        theta_2 = -np.deg2rad(tibia_rest_heading)
    else:
        beta = cosine_rule_from_sides([femur_len, tibia_len], d)
        alpha = cosine_rule_from_sides([femur_len, d], tibia_len)
        descent_angle = math.atan2(-d_vec[2], d_vec[1])
        theta_1 = descent_angle - alpha - np.deg2rad(femur_rest_heading)
        theta_2 = math.pi - beta - np.deg2rad(tibia_rest_heading)
    
    theta_0 = clamp_angle(-100, 100, np.rad2deg(theta_0))
    theta_1 = clamp_angle(-100, 100, np.rad2deg(theta_1))
    theta_2 = clamp_angle(-100, 100, np.rad2deg(theta_2))
    
    
    return np.array([theta_0, theta_1, theta_2])


def clamp_angle(lower, upper, angle):
    if angle < lower:
        return lower
    if angle > upper:
        return upper
    return angle