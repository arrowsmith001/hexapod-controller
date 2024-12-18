from model.hexapod import *
from utils.ik import trajectory_as_angles
from utils.move import *
from utils.servo import *
from config import *
import time
import math
import numpy as np

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
        target = position + movement_vector
        angles = trajectory_as_angles(position, target, ms, leg.heading)
        dt = 0.025
        steps = int(ms / dt)
        for i in range(steps):
            right_back_leg.set_angles(angles[i])
            time.sleep(dt)
        position = target
        

while True:
    print('loop')

    add_move([0, 0, 50], 250)
    add_move([0, 100, 50], 250)
    add_move([0, 100, 0], 250)
    add_move([0, 0, 0], 250)
    move()