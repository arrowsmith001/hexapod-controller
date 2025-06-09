from hexapod.leg_position import LegType
import numpy as np

class Motion:
    def __init__(self, vector, start_time, duration, leg: LegType, t_start=0.0, t_end=1.0):
        self.vector = np.array(vector)
        self.start = start_time
        self.duration = duration
        self.leg = leg
        self.t_start = t_start
        self.t_end = t_end
        
    """Check if the motion is active at time t."""
    def is_active(self, t):
        return self.start <= t < self.start + self.duration
    
    def interp(self, start_pos, t):
        """Interpolate between start_pos and end_pos at time t."""
        raise NotImplementedError("Subclasses must implement interp")

class LinearMotion(Motion):
    
    def __init__(self, vector, start_time, duration, leg: LegType, t_start=0.0, t_end=1.0, useDelta=False):
        super().__init__(vector, start_time, duration, leg, t_start, t_end)
        self.useDelta = useDelta
    
    """Interpolate linearly at time t."""
    def interp(self, start_pos, t):
        raw_t = np.clip((t - self.start) / self.duration, 0, 1)
        _t = self.t_start + (self.t_end - self.t_start) * raw_t
        return start_pos + _t * self.vector
        

class BezierMotion(Motion):
    
    def __init__(self, vector, start_time, duration, leg: LegType, control_point, t_start=0.0, t_end=1.0):
        super().__init__(vector, start_time, duration, leg, t_start, t_end)
        self.control_point = np.array(control_point)
        
    """Interpolate using a Bezier curve with one control point at time t."""
    def interp(self, start_pos, t):
        # Normalized time in [0, 1]
        raw_t = np.clip((t - self.start) / self.duration, 0, 1)
        _t = self.t_start + (self.t_end - self.t_start) * raw_t

        start_pos = np.array(start_pos)
        control_point = start_pos + self.control_point
        end_pos = np.array(start_pos + self.vector)
        return((1 - _t) ** 2) * start_pos + \
               2 * (1 - _t) * _t * control_point + \
               (_t ** 2) * end_pos
               

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
        
    """Get all motions for a specific leg in time order."""
    def get_leg_motions_in_time_order(self, leg: LegType):
        return sorted((motion for motion in self.motions if motion.leg == leg), key=lambda m: m.start)
    
    """Get the count of motions for a specific leg."""
    def get_leg_motion_count(self, leg: LegType):
        return sum(1 for motion in self.motions if motion.leg == leg)
    
    """Get the motion for a specific leg at time t."""
    def get_leg_motion_at_time(self, leg: LegType, t):
        for idx, motion in enumerate(self.motions):
            if motion.leg != leg:
                continue
            if motion.is_active(t):
                return motion, idx
        return None, None
    
    duration = 0