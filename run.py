#!/usr/bin/python

from model.hexapod import *
from utils.move import *
from utils.servo import *
from config import *
import time
import math

#kill_servos()

while True:
    print("hello")
    time.sleep(0.1)
    #break
    j2_target = 60
    j3_target = 60
    secs = 0.1

    lift_angle = 30
    sweep_angle = 60
    dt = 0.025


    back_right_j0_pos = [-39.5, -61, -22]
    back_right_rest_foot_measured = [-111, -133, -83]
    back_right_rest_angles = [0, 0, 0]
    
    back_right_offset = [back_right_rest_foot_measured[0] - back_right_j0_pos[0], back_right_rest_foot_measured[1] - back_right_j0_pos[1], back_right_rest_foot_measured[2] - back_right_j0_pos[2]]
    print("back_right_offset: ", back_right_offset)
    
    movement_vector = [-100, 300, 0]
    # TODO: Once movement vector and target has been confirmed, calculate R to rotate everything and calculate normalized 
    trajectory = []
    
    def leg_ik(j0_pos, target):
        x, y, z = target
        j0_x, j0_y, j0_z = j0_pos
        
        dx = x - j0_x
        dy = y - j0_y
        dz = z - j0_z
        
        
        print("dx: ", dx, "dy: ", dy, "dz: ", dz)
        
        theta1 = math.atan2(dy, dx)
        theta1 = rad2deg(theta1)
        

        return [theta1, 0, 0]
    
    steps = 100
    
    # generate trajectory
    for i in range(steps):
        step = [back_right_rest_foot_measured[0] + i * movement_vector[0] / steps, back_right_rest_foot_measured[1] + i * movement_vector[1] / steps, back_right_rest_foot_measured[2] + i * movement_vector[2] / steps]
        step2angles = leg_ik(back_right_j0_pos, step)
        trajectory.append(step2angles)
        print('step: ', step, 'step2angles: ', step2angles)
        # time.sleep(0.1)
    # move along trajectory
    for i in range(steps):
        move_joints_linear([hexapod.right_back_leg.joints[0], hexapod.right_back_leg.joints[1], hexapod.right_back_leg.joints[2]], trajectory[i], dt)
        time.sleep(dt)
        
        
    
    #move_joint_linear(hexapod.right_back_leg.joints[1], lift_angle, dt)



    # move_legs_linear([right_front_leg, right_back_leg, left_front_leg, left_back_leg],
    #     [[
    #         0, j2_target, j3_target
    #     ],[
    #         0, j2_target, j3_target
    #     ],[
    #         0, j2_target, j3_target
    #     ],[
    #         0, j2_target, j3_target
    #     ]], secs)
    
    # move_legs_linear([right_front_leg, right_back_leg, left_front_leg, left_back_leg],
    #     [[
    #         0, -j2_target, -j3_target
    #     ],[
    #         0, -j2_target, -j3_target
    #     ],[
    #         0, -j2_target, -j3_target
    #     ],[
    #         0, -j2_target, -j3_target
    #     ]], secs)

    # Moves leg in a triangle
    # move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [-45, -45, -45], 0.5) # fwd, up, up
    # move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [45, -90, -45], 0.5) # move across
    # move_joints([right_mid_j0, right_mid_j1, right_mid_j2], [0, 0, 0],  0.5) # back to start
    # move legs asynch
    # move_leg(test_leg, [45, 45, 45], 2)
    # move_leg(test_leg, [0, 0, 0], 2)
    # move_leg(test_leg, [-45, -45, -45], 2)
    
    #move_leg(right_mid_leg, [0, 0, 0], 1)
    #move_leg(right_mid_leg, [0, 0, 0], 1)

    # # Position of first joint - fixed relative to body
    # right_mid_j1 = [49.359, 1.496, -21.97]

    # # Going to work with relative target for now

    # # iterate over a small circle in x-y plane
    # for i in range(100):
    #     x = 50 * math.cos(i * 2 * math.pi / 100)
    #     y = 50 * math.sin(i * 2 * math.pi / 100)
    #     z = 0
    #     move_leg_ik(right_mid_leg, [x, y, z], 0.05)


    #move_leg(right_mid_leg, [-45, -45, -45], 1)
    # move_leg(right_mid_leg, [90, 0, 0], 1)
    # move_leg(right_mid_leg, [0, 0, 0], 1)
    # move_leg(right_mid_leg, [0, 0, 0], 1)
    # move_leg(right_mid_leg, [0, 90, 0], 1)
    # move_leg(right_mid_leg, [0, 0, 0], 1)
    # move_leg(right_mid_leg, [0, 0, 90], 1)



    # move_legs(
    #     [right_mid_leg, right_front_leg, right_back_leg, left_front_leg, left_mid_leg, left_back_leg], 
    #     [[45, 45, 45],[45, 45, 45],[45, 45, 45],[45, 45, 45],[45, 45, 45],[45, 45, 45]], 0.5)
    # move_legs(
    #     [right_mid_leg, right_front_leg, right_back_leg, left_front_leg, left_mid_leg, left_back_leg], 
    #     [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]], 0.5)
        
    # kill_servos()
    # time.sleep(1)
    