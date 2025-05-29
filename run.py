from motion import Gait, LinearMotion
from config import *
from leg_position import LegPosition
import time

# A gait is defined by a set of movements, each with either a LinearMotion or BezierMotion, and a start and end time
wave_gait = Gait([
    LinearMotion([0, 30, 0], 0, 1000, LegPosition.LEFT_FRONT),
    LinearMotion([0, -30, 0], 1000, 1000, LegPosition.LEFT_MID),
    LinearMotion([0, 30, 0], 2000, 1000, LegPosition.LEFT_BACK),
    LinearMotion([0, -30, 0], 3000, 1000, LegPosition.RIGHT_FRONT),
    LinearMotion([0, 30, 0], 4000, 1000, LegPosition.RIGHT_MID),
    LinearMotion([0, -30, 0], 5000, 1000, LegPosition.RIGHT_BACK)
])

# Give the hexapod a gait
hexapod.set_gait(wave_gait)

# Generate the leg angles for the gait, granularity specified by delta
hexapod.compute_joint_angles(delta=0.01)

while True:
    print('loop')
    
    t = 0
    dt = 0.025
    
    # Keep incrementing time by dt, and set the angles for the hexapod at each time
    while t < hexapod.gait.duration:
        hexapod.set_angles_at(t)
        t += dt
        time.sleep(dt)