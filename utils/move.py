import math
import time
from hexapod.constants import coxa_len, femur_len, tibia_len
from numpy import rad2deg
from model.hexapod_leg_joint import HexapodLegJoint
from model.hexapod import HexapodLegJoint, HexapodLeg

# These are test functions, currently not used in main control program

def move_joint_linear(joint : HexapodLegJoint, target_angle, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angle = joint.get_angle()
    angle_step = (target_angle - start_angle) / steps
    for i in range(steps):
        joint.set_angle(start_angle + i * angle_step)
        time.sleep(dt)

def move_joints_linear(joints, target_angles, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angles = [j.get_angle() for j in joints]
    angle_steps = [(target_angles[i] - start_angles[i]) / steps for i in range(len(joints))]
    for i in range(steps):
        for j in range(len(joints)):
            joints[j].set_angle(start_angles[j] + i * angle_steps[j])

        print(int(joints[0].get_angle()), int(joints[1].get_angle()), int(joints[2].get_angle()))
        time.sleep(dt)

def move_leg_linear(leg : HexapodLeg, target_angles, seconds, dt=0.005):
    move_joints_linear(leg.joints, target_angles, seconds, dt)

def move_legs_linear(legs, target_angles, seconds, dt=0.01):
    # expand all joints and targets into a massive array to pass to move_joints
    joints_ext = []
    target_angles_ext = []
    for i in range(len(legs)):
        joints_ext.extend(legs[i].joints)
        target_angles_ext.extend(target_angles[i])
    move_joints_linear(joints_ext, target_angles_ext, seconds, dt)

# Deprecated
def move_leg_ik(leg : HexapodLeg, target, dt=0.01):
    rel_target = [target[0] - leg.origin[0], target[1] - leg.origin[1], target[2] - leg.origin[2]]
    
    if rel_target[0] != 0:
        theta1 = math.atan(rel_target[1]/rel_target[0])
    else:
        theta1 = 90 if rel_target[1] > 0 else -90

    l1 = math.sqrt(rel_target[0]**2 + rel_target[1]**2) # distance from first joint to rel_target in x-y plane
    l2 = math.fabs(l1 - coxa_len) # distance from second joint to rel_target 

    cos_theta21 = (tibia_len**2 - femur_len**2 - l2**2)/(2*femur_len*l2)
    theta21 = math.acos(max(-1, min(1, cos_theta21))) # angle between 2nd joint to rel_target and 2nd joint to 3rd joint
    
    theta22 = math.atan(rel_target[2]/l2) # angle between 2nd joint and rel_target
    theta2 = theta21 + theta22

    cos_theta3 = (l2**2 - femur_len**2 - tibia_len**2)/(2*femur_len*tibia_len)
    theta3 = max(-1, min(1, cos_theta3)) # angle between 3rd joint and rel_target
    
    print(int(theta1 * (360 / (math.pi * 2))), int(theta2 * (360 / (math.pi * 2))), int(theta3 * (360 / (math.pi * 2))))

    move_leg_linear(leg, [rad2deg(theta1) + 45, 0, 0], dt)

