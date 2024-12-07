
import math
import time

from model.hexapod import *
from config import *
from numpy import rad2deg


def move_joint(joint : HexapodLegJoint, target_angle, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angle = joint.get_angle()
    angle_step = (target_angle - start_angle) / steps
    for i in range(steps):
        joint.set_angle(start_angle + i * angle_step)
        time.sleep(dt)

def move_joints(joints, target_angles, seconds, dt=0.01):
    steps = int(seconds / dt)
    start_angles = [j.get_angle() for j in joints]
    angle_steps = [(target_angles[i] - start_angles[i]) / steps for i in range(len(joints))]
    for i in range(steps):
        for j in range(len(joints)):
            joints[j].set_angle(start_angles[j] + i * angle_steps[j])

        print(int(joints[0].get_angle()), int(joints[1].get_angle()), int(joints[2].get_angle()))
        time.sleep(dt)

def move_leg(leg : HexapodLeg, target_angles, seconds, dt=0.005):
    move_joints(leg.joints, target_angles, seconds, dt)

def move_legs(legs, target_angles, seconds, dt=0.01):
    # expand all joints and targets into a massive array to pass to move_joints
    joints_ext = []
    target_angles_ext = []
    for i in range(len(legs)):
        joints_ext.extend(legs[i].joints)
        target_angles_ext.extend(target_angles[i])
    move_joints(joints_ext, target_angles_ext, seconds, dt)

        
def move_leg_ik(leg : HexapodLeg, target, dt=0.01):
    
    theta1 = math.atan(target[1]/target[0])

    l1 = math.sqrt(target[0]**2 + target[1]**2) # distance from first joint to target in x-y plane
    l2 = math.fabs(l1 - coxa_len) # distance from second joint to target 

    cos_theta21 = (tibia_len**2 - femur_len**2 - l2**2)/(2*femur_len*l2)
    theta21 = math.acos(max(-1, min(1, cos_theta21))) # angle between 2nd joint to target and 2nd joint to 3rd joint
    
    theta22 = math.atan(target[2]/l2) # angle between 2nd joint and target
    theta2 = theta21 + theta22

    cos_theta3 = (l2**2 - femur_len**2 - tibia_len**2)/(2*femur_len*tibia_len)
    theta3 = max(-1, min(1, cos_theta3)) # angle between 3rd joint and target
    

    print(int(theta1 * (360 / (math.pi * 2))), int(theta2 * (360 / (math.pi * 2))), int(theta3 * (360 / (math.pi * 2))))

    move_leg(leg, [theta1 * rad2deg, theta2 * rad2deg, theta3 * rad2deg], dt)

