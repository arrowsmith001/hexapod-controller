from hexapod.leg_position import LegType
import numpy as np


class Motion:
    def __init__(self, vector, start_time, duration, leg: LegType):
        self.vector = np.array(vector)
        self.start = start_time
        self.duration = duration
        self.leg = leg
        print('Initialized motion:', self.leg, 'vector:', self.vector, 'start:', self.start, 'duration:', self.duration)
        
    """Check if the motion is active at time t."""
    def is_active(self, t):
        return self.start <= t < self.start + self.duration
        
    """Interpolate between start_pos and end_pos at time t."""
    def interp(self, start_pos, t):
        pass

class LinearMotion(Motion):
    
    """Interpolate linearly at time t."""
    def interp(self, start_pos, t):
        local_t = np.clip((t - self.start) / self.duration, 0, 1)
        return start_pos + local_t * self.vector
        

class BezierMotion(Motion):
    
    def __init__(self, vector, start_time, duration, leg: LegType, control_point):
        super().__init__(vector, start_time, duration, leg)
        self.control_point = np.array(control_point)
        
    """Interpolate using a Bezier curve with one control point at time t."""
    def interp(self, start_pos, t):
        local_t = np.clip((t - self.start) / self.duration, 0, 1)
        start_pos = np.array(start_pos)
        control_point = start_pos + self.control_point
        end_pos = np.array(start_pos + self.vector)
        return ((1 - local_t) ** 2) * start_pos + \
               2 * (1 - local_t) * local_t * control_point + \
               (local_t ** 2) * end_pos

class Pause(Motion):
    def __init__(self, start_time, duration, leg: LegType):
        super().__init__([], start_time, duration, leg)
        
    def interp(self, start_pos, t):
        return start_pos

class Gait:
    def __init__(self, motions: list[Motion]):
        self.motions = motions
        
        if len(motions) != 0:
            self.duration = max(motion.start + motion.duration for motion in motions)
        
        # Validate that all motions are non-overlapping for each leg
        self.validate_motions()
        
    """Ensure that no two motions for the same leg overlap in time."""
    def validate_motions(self):
        for leg in LegType:
            leg_motions = self.get_leg_motions_in_time_order(leg)
            for i in range(len(leg_motions) - 1):
                if leg_motions[i].start + leg_motions[i].duration > leg_motions[i + 1].start:
                    raise ValueError(f"Overlapping motions detected for leg {leg}. "
                                     f"{leg_motions[i]} overlaps with {leg_motions[i + 1]}.")
        
    """Get all motions for a specific leg in time order."""
    def get_leg_motions_in_time_order(self, leg: LegType):
        return sorted((motion for motion in self.motions if motion.leg == leg), key=lambda m: m.start)
    
    """Get the count of motions for a specific leg."""
    def get_leg_motion_count(self, leg: LegType):
        return sum(1 for motion in self.motions if motion.leg == leg)
    
    """Get the motion for a specific leg at time t."""
    def get_leg_motion_at_time(self, leg: LegType, t):
        for motion in self.get_leg_motions_in_time_order(leg):
            if motion.is_active(t):
                return motion
        return None
    
    duration = 0