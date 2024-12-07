from model.hexapod import *

# Lengths of the leg segments in mm

coxa_len = 34.124
femur_len = 48.325
tibia_len = 72.652

# I use a 32-channel Pi Hat which uses 2 different I2C addresses each with up to 16 PWM channels: 
#   - 0-1 for the PWM channel
#   - 0-15 for the port number

left_front_ports = [[0,12], [0,13], [0,14]]
left_mid_ports = [[1,0], [0,1], [0,2]]
left_back_ports = [[1,7], [1,8], [1,9]]

right_front_ports = [[0,4], [0,5], [0,6]]
right_mid_ports = [[0,0], [0,1], [0,2]]
right_back_ports = [[0,4], [0,5], [0,6]]

left_front_leg = HexapodLeg(
    HexapodLegJoint(left_front_ports[0]), 
    HexapodLegJoint(left_front_ports[1]), 
    HexapodLegJoint(left_front_ports[2]))

left_back_leg = HexapodLeg(
    HexapodLegJoint(left_back_ports[0]), 
    HexapodLegJoint(left_back_ports[1]), 
    HexapodLegJoint(left_back_ports[2]))

right_front_leg = HexapodLeg(
    HexapodLegJoint(right_front_ports[0]), 
    HexapodLegJoint(right_front_ports[1]), 
    HexapodLegJoint(right_front_ports[2]))

right_back_leg = HexapodLeg(
    HexapodLegJoint(right_back_ports[0]), 
    HexapodLegJoint(right_back_ports[1]), 
    HexapodLegJoint(right_back_ports[2]))

# left_mid_leg = HexapodLeg(
#     HexapodLegJoint(left_mid_ports[0]), 
#     HexapodLegJoint(left_mid_ports[1]), 
#     HexapodLegJoint(left_mid_ports[2]))

# right_mid_leg = HexapodLeg(
#     HexapodLegJoint(right_mid_ports[0]), 
#     HexapodLegJoint(right_mid_ports[1]), 
#     HexapodLegJoint(right_mid_ports[2]))

hexapod = Hexapod(left_front_leg, None, left_back_leg, right_front_leg, None, right_back_leg)