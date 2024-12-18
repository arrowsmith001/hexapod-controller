from model.hexapod import *
import math

from model.hexapod import HexapodLeg

# Lengths of the leg segments in mm

coxa_len = 24.6
coxa_elevation = 14
femur_len = 47.5
tibia_len = 70.3

# I use a 32-channel Pi Hat which uses 2 different I2C addresses each with up to 16 PWM channels: 
#   - 0-1 for the PWM channel
#   - 0-15 for the port number

left_front_ports = [[0,2], [0,1], [0,0]]
left_back_ports = [[1,13], [1,14], [1,15]]

right_front_ports = [[0,10], [0,9], [0,8]]
right_back_ports = [[1,5], [1,6], [1,7]]

left_mid_ports = [[1,0], [0,1], [0,2]]
right_mid_ports = [[1,0], [0,1], [0,2]]

left_front_leg = HexapodLeg([], 0,
    HexapodLegJoint(left_front_ports[0], initial_angle=-30), 
    HexapodLegJoint(left_front_ports[1]), 
    HexapodLegJoint(left_front_ports[2]))

left_back_leg = HexapodLeg([], 0,
    HexapodLegJoint(left_back_ports[0], initial_angle=-30), 
    HexapodLegJoint(left_back_ports[1]), 
    HexapodLegJoint(left_back_ports[2]))

right_front_leg = HexapodLeg([], 0,
    HexapodLegJoint(right_front_ports[0], invert=True, initial_angle=-30), 
    HexapodLegJoint(right_front_ports[1], invert=True), 
    HexapodLegJoint(right_front_ports[2], invert=True))

right_back_leg = HexapodLeg([39.435, -61.125, -21.970], 135,
    HexapodLegJoint(right_back_ports[0], invert=False, angle_offset=4), 
    HexapodLegJoint(right_back_ports[1], invert=False), 
    HexapodLegJoint(right_back_ports[2], invert=True, angle_offset=15))

# left_mid_leg = HexapodLeg(
#     HexapodLegJoint(left_mid_ports[0]), 
#     HexapodLegJoint(left_mid_ports[1]), 
#     HexapodLegJoint(left_mid_ports[2]))

# right_mid_leg = HexapodLeg(
#     HexapodLegJoint(right_mid_ports[0]), 
#     HexapodLegJoint(right_mid_ports[1]), 
#     HexapodLegJoint(right_mid_ports[2]))

hexapod = Hexapod(left_front_leg, None, left_back_leg, right_front_leg, None, right_back_leg)