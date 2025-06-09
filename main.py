from hexapod.config import *
import time
from hexapod.gaits import wave_gait_1, ripple_gait_init, ripple_gait, ripple_left_turn, ripple_right_turn, tripod_gait, tripod_left_turn, bob
import utils.move

# Add named gaits to the hexapod
hexapod.add_gait("walk_start", ripple_gait_init)
hexapod.add_gait("walk_continuous", ripple_gait)

# Generate the leg angles for all added gaits, granularity specified by delta
hexapod.compute_joint_angles(dt=0.01)

while True:
    
    t = 0
    dt = 0.025
    
    hexapod.set_active_gait("walk_start")
    
    while t < hexapod.get_active_gait().duration:
        hexapod.set_angles_at(t)
        t += dt
        time.sleep(dt)
        
    hexapod.set_active_gait("walk_continuous")
    
    while True:
        t = 0
        while t < hexapod.get_active_gait().duration:
            hexapod.set_angles_at(t)
            t += dt
            time.sleep(dt)