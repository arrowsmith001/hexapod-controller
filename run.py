import numpy as np
from utils.ik import trajectory_as_angles
from utils.move import *
from utils.servo import *
from config import right_back_leg
import time

#kill_servos()

movements = []
def add_move(movement_vector, ms):
    movements.append([movement_vector, ms])

def move():
    leg = right_back_leg
    position = leg.foot_rest_position
    for movement in movements:
        movement_vector = movement[0]
        ms = movement[1]
        target = np.array(position) + np.array(movement_vector)
        angles = trajectory_as_angles(position, target, ms, leg.heading)
        dt = 0.025
        steps = int(ms / dt)
        print('angles: ' + str(len(angles)), 'by', str(len(angles[0])))
        for i in range(steps):
            right_back_leg.set_angles(angles[i])
            time.sleep(dt)
        position = target
        

while True:
    print('loop')
    
    move_joint_linear(HexapodLegJoint([1, 11]), 90, 1)    
    time.sleep(1)
    move_joint_linear(HexapodLegJoint([1, 11]), 0, 1)    
    time.sleep(1)
    
    # right_back_leg.set_angles([0, 0, 0])
    
    # start_pos = right_back_leg.foot_rest_position
    # movement_vector = np.array([200, 200, 200])
    
    # target = start_pos + movement_vector
    # duration = 2000
    # dt = 10
    # steps = int(duration / dt)
    # print('steps: ' + str(steps))
    
    # angles = trajectory_as_angles(start_pos, target, steps, 135)
    # # print(str(angles))
    # print('angles: ' + str(len(angles)), 'by', str(len(angles[0])))
    # for i in range(steps):
    #     right_back_leg.set_angles(angles[i])
    #     time.sleep(dt / 1000)
    