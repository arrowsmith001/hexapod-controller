#!/usr/bin/python

from model.hexapod import *
from utils.servo import *
from config import *
import time
import math


while True:
    print("hello")
    time.sleep(0.1)
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
    
  

# femur_len = 48.325
# # Right leg config
# theta0 = math.atan(targ[1]/targ[0])
# theta1 = 