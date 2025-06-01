import numpy as np
from hexapod.motion import Gait, LinearMotion, BezierMotion
from hexapod.config import *
from utils.ik import leg_ik
from hexapod.leg_position import LegType
import time
import math
from utils.move import move_joint_linear

# Testing variables
test_x = 0#50
test_y = 0#-61.25
test_z = 50

reach = 30
elevation = -30
control_height = 30

dur = 0.15
interval = 0.1 
m = 0.5
delay = 0.1

# A gait is defined by a set of movements, each with either a LinearMotion or BezierMotion, and a start and end time
test_gait = Gait([
    LinearMotion([-reach, -reach, elevation], 0, dur, LegType.LEFT_BACK),
    LinearMotion([reach, reach, -elevation], dur, dur, LegType.LEFT_BACK),
    LinearMotion([-reach, 0, elevation], 0+delay, dur, LegType.LEFT_MID),
    LinearMotion([reach, 0, -elevation], 0+delay+dur, dur, LegType.LEFT_MID),
    LinearMotion([-reach, reach, elevation], 0+2*delay, dur, LegType.LEFT_FRONT),
    LinearMotion([reach, -reach, -elevation], 0+2*delay+dur, dur, LegType.LEFT_FRONT),
    LinearMotion([reach, reach, elevation], 0+3*delay, dur, LegType.RIGHT_FRONT),
    LinearMotion([-reach, -reach, -elevation], 0+3*delay + dur, dur, LegType.RIGHT_FRONT),
    LinearMotion([reach, 0, elevation], 0+4*delay, dur, LegType.RIGHT_MID),
    LinearMotion([-reach, 0, -elevation], 0+4*delay + dur, dur, LegType.RIGHT_MID),
    LinearMotion([reach, -reach, elevation], 0+5*delay, dur, LegType.RIGHT_BACK),
    LinearMotion([-reach, reach, -elevation], 0+5*delay+dur, dur, LegType.RIGHT_BACK),
    
    # BezierMotion([-reach / math.sqrt(2), -reach / math.sqrt(2), elevation], 0, 3, LegType.LEFT_BACK, [-reach*0.8, -reach*0.8, control_height]),
    # BezierMotion([reach / math.sqrt(2), reach / math.sqrt(2), -elevation], 3, 3, LegType.LEFT_BACK, [-reach*0.8, -reach*0.8, control_height]),
    # BezierMotion([-reach, 0, elevation], 0, 3, LegType.LEFT_MID, [-reach*0.8, 0, control_height]),
    # BezierMotion([reach, 0, -elevation], 3, 3, LegType.LEFT_MID, [-reach*0.8, 0, control_height]),
    # BezierMotion([-reach, reach / math.sqrt(2), elevation], 0, 3, LegType.LEFT_FRONT, [-reach*0.8, reach*0.8, control_height]),
    # BezierMotion([reach, -reach / math.sqrt(2), -elevation], 3, 3, LegType.LEFT_FRONT, [-reach*0.8, -reach*0.8, control_height]),
    
    # BezierMotion([reach, -reach / math.sqrt(2), elevation], 0, 3, LegType.RIGHT_BACK, [reach*0.8, -reach*0.8, control_height]),
    # BezierMotion([-reach, reach / math.sqrt(2), -elevation], 3, 3, LegType.RIGHT_BACK, [reach*0.8, -reach*0.8, control_height]),
    # BezierMotion([reach, 0, elevation], 0, 3, LegType.RIGHT_MID, [reach*0.8, 0, control_height]),
    # BezierMotion([-reach, 0, -elevation], 3, 3, LegType.RIGHT_MID, [reach*0.8, 0, control_height]),
    # BezierMotion([reach, reach / math.sqrt(2), elevation], 0, 3, LegType.RIGHT_FRONT, [reach*0.8, reach*0.8, control_height]),
    # BezierMotion([-reach, -reach / math.sqrt(2), -elevation], 3, 3, LegType.RIGHT_FRONT, [reach*0.8, -reach*0.8, control_height]),
    
])

#Give the hexapod a gait
hexapod.set_gait(test_gait)

# Generate the leg angles for the gait, granularity specified by delta
hexapod.compute_joint_angles(delta=0.01)

#move_joint_linear(hexapod.get_leg(LegType.RIGHT_BACK).joints[1], 45, 1)

while True:
    
    t = 0
    dt = 0.025
    
    # # Keep incrementing time by dt, and set the angles for the hexapod at each time
    while t < hexapod.gait.duration:
        hexapod.set_angles_at(t)
        angles = hexapod.get_leg(LegType.LEFT_FRONT).get_angles()
        poscheck = hexapod.get_leg(LegType.LEFT_FRONT).get_foot_position_at_angles(np.array(angles))
        #print(f"Time: {t:.2f}s, Angles: {angles}")
        t += dt
        print('t:', t)
        time.sleep(dt)