import numpy as np
from hexapod.config import *
from utils.ik import leg_ik
from hexapod.leg_position import LegType
import time
import math
from utils.move import move_joint_linear
from hexapod.gaits import wave_gait_1 as wave_gait

#Give the hexapod a gait
hexapod.set_gait(wave_gait)

# Generate the leg angles for the gait, granularity specified by delta
hexapod.compute_joint_angles(delta=0.01)

while True:
    
    t = 0
    dt = 0.01
    
    # # Keep incrementing time by dt, and set the angles for the hexapod at each time
    while t < hexapod.gait.duration:
        hexapod.set_angles_at(t)
        t += dt
        time.sleep(dt)