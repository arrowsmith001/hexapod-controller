

from leg_position import LegPosition
import numpy as np


class Motion:
    def __init__(self, vector, start_time, duration, leg: LegPosition):
        self.vector = vector
        self.start = start_time
        self.duration = duration
        self.leg = leg
        
    def is_active(self, t):
        """Check if the motion is active at time t."""
        return self.start <= t < self.start + self.duration
        
    def interp(self, start_pos, end_pos, t):
        """Interpolate between start_pos and end_pos at time t."""
        pass

class LinearMotion(Motion):
    
    def interp(self, start_pos, end_pos, t):
        """Interpolate linearly between start_pos and end_pos at time t."""
        local_t = np.clip((t - self.start) / self.duration, 0, 1)
        return start_pos + (end_pos - start_pos) * local_t
        

class BezierMotion(Motion):
    def __init__(self, control_point, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control_point = control_point  # Control point for Bezier curve
    
    def interp(self, start_pos, end_pos, t):
        """Interpolate using a Bezier curve defined by start_pos, control_point, and end_pos at time t."""
        local_t = np.clip((t - self.start) / self.duration, 0, 1)
        return (1 - local_t)**2 * start_pos + \
               2 * (1 - local_t) * local_t * self.control_point + \
               local_t**2 * end_pos

class Gait:
    def __init__(self, motions: list[Motion]):
        self.motions = motions  # List of Motion instances
        self.duration = max(motion.start + motion.duration for motion in motions)
        
        # Validate that all motions are non-overlapping for each leg
        self.validate_motions()
        
    def validate_motions(self):
        """Ensure that no two motions for the same leg overlap in time."""
        leg_motions = {}
        for motion in self.motions:
            if motion.leg not in leg_motions:
                leg_motions[motion.leg] = []
            leg_motions[motion.leg].append(motion)
        
        for leg, motions in leg_motions.items():
            motions.sort(key=lambda m: m.start)
            for i in range(1, len(motions)):
                if motions[i].start < motions[i-1].start + motions[i-1].duration:
                    raise ValueError(f"Overlapping motions detected for leg {leg}: {motions[i]} overlaps with {motions[i-1]}")
        
    def get_leg_motions_in_time_order(self, leg: LegPosition):
        """Get all motions for a specific leg in time order."""
        return sorted((motion for motion in self.motions if motion.leg == leg), key=lambda m: m.start)