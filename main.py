from hexapod.config import *
import time
from hexapod.gaits import ripple_gait_init, ripple_gait

# Add named gaits to the hexapod
hexapod.add_gait("walk_start", ripple_gait_init)
hexapod.add_gait("walk_continuous", ripple_gait)

# Generate the leg angles for all added gaits, granularity specified by delta
hexapod.compute_joint_angles(delta=0.01)

while True:
    
    t = 0
    dt = 0.01
    
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