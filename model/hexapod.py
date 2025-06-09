import numpy as np
from hexapod.leg_position import LegType
from hexapod.motion import Gait
from model.hexapod_leg import HexapodLeg
from utils.servo import *
from hexapod.constants import *
from utils.ik import leg_ik
    

class Hexapod:
    
    gaits: dict[str, Gait] = {}
    angles: dict[str, np.ndarray] = {}
    active_gait: str = ''

    def __init__(self, legs : list[HexapodLeg]):
        # For each leg, its type is deduced. 
        # The hexapods surrounding area is divided into 6 equal sections. Then the angle is read to determine the leg's position.
        self.legs: list[HexapodLeg | None] = [None] * 6
        for i in range(len(legs)):
            leg: HexapodLeg = legs[i]
            leg_heading = leg.joint_rest_headings[0]
            type = None or LegType
            if leg_heading > -180 and leg_heading < 0:
                # Left side legs
                if leg_heading < -120:
                    type = LegType.LEFT_BACK
                elif leg_heading < -60:
                    type = LegType.LEFT_MID
                else:
                    type = LegType.LEFT_FRONT
            elif leg_heading >= 0 and leg_heading < 180:
                # Right side legs
                if leg_heading < 60:
                    type = LegType.RIGHT_FRONT
                elif leg_heading < 120:
                    type = LegType.RIGHT_MID
                else:
                    type = LegType.RIGHT_BACK
            else:
                raise ValueError("Invalid leg heading: " + str(leg_heading))
            if self.legs[type.value] is not None:
                conflicting_leg = self.legs[type.value]
                conflict_heading = conflicting_leg.leg_heading if conflicting_leg is not None else None
                raise ValueError("Duplicate leg heading: " + str(leg_heading) + " conflicts with " + str(conflict_heading))
            self.legs[type.value] = leg
            
    def add_gait(self, label, gait: Gait):
        if not hasattr(self, 'gaits'):
            self.gaits = {}
        if label in self.gaits:
            raise ValueError("Gait with label " + label + " already exists")
        self.gaits[label] = gait
            
    def get_leg(self, position: LegType):
        if position.value < 0 or position.value >= len(self.legs):
            raise ValueError("Invalid leg position")
        leg = self.legs[position.value]
        if leg is None:
            raise ValueError("Leg at position " + position.name + " is not set")
        return leg
    
    def compute_joint_angles(self, dt=0.1):
        
        for key, gait in self.gaits.items():
            
            if gait.duration <= 0:
                raise ValueError("Gait duration must be greater than 0")
            
            total_steps = int(gait.duration / dt)
            
            angles = np.empty([total_steps, len(self.legs), 3], dtype=float)
        
            # One leg at a time in time order (since the absolute position needs to be calculated)
            for i in range(len(self.legs)):
                leg = self.legs[i]
                if leg is None:
                    continue
                
                # Start with the initial angles for this leg
                leg_type = LegType(i)
                leg_origin = leg.origin
                
                # Get motion count for this leg
                motion_count = gait.get_leg_motion_count(leg_type)
                
                current_angles = leg.starting_angles
                current_reference_pos = leg.get_foot_position_at_angles(current_angles)
                current_time = 0
                current_motion_index = None
                #current_pos = leg.get_foot_position_at_angles(current_angles) - leg_origin
                
                #print('Starting angles: ', current_angles, 'for leg:', leg_type.name)
                #print('Starting reference position:', current_reference_pos, 'for leg:', leg_type.name)
                print('leg_ik check:', leg_ik(current_reference_pos - leg_origin, leg.joint_rest_headings), 'for leg: ', leg_type.name)
                
                for i in range(total_steps):
                    
                    if motion_count == 0:
                        # No motions for this leg, just use the initial angles
                        angles[i, leg_type.value, :] = leg.starting_angles
                        continue
                    
                    current_time = i * dt
                    current_motion, current_motion_index = gait.get_leg_motion_at_time(leg_type, current_time)
                    
                    if current_motion is None:
                        # No motion at this time, use the last known angles
                        angles[i, leg_type.value, :] = current_angles
                        continue
                    
                    # Calculate target position
                    pos = current_motion.interp(current_reference_pos - leg_origin, current_time)
                    
                    # Calculate the angles for this position
                    _angles = leg_ik(pos, leg.joint_rest_headings)  
                    
                    # Set angles
                    angles[i, leg_type.value, :] = _angles
                    
                    current_angles = _angles
                    
                    # If next motion is different, update the reference position
                    _, next_motion_index = gait.get_leg_motion_at_time(leg_type, current_time + dt)
                    if next_motion_index != current_motion_index:
                        print(current_time, ':', 'Switching motion index: ', current_motion_index, 'to', next_motion_index, 'for leg:', leg_type.name)
                        current_reference_pos = pos + leg_origin
                        
            self.angles[key] = angles
        
    def set_active_gait(self, label: str):
        if label not in self.gaits:
            raise ValueError("Gait with label " + label + " does not exist")
        self.active_gait = label
        
    def get_active_gait(self) -> Gait:
        if self.active_gait is None or self.active_gait not in self.gaits:
            raise ValueError("No active gait set. Call set_gait() first.")
        return self.gaits[self.active_gait]
            
    def set_angles_at(self, time: float):
        if not hasattr(self, 'angles'):
            raise ValueError("Angles not computed. Call compute_joint_angles() first.")
        
        if self.active_gait is None or self.active_gait not in self.gaits:
            raise ValueError("No active gait set. Call set_gait() first.")
        
        gait: Gait = self.get_active_gait()
        
        if time < 0 or time >= gait.duration:
            time = time % gait.duration  # Wrap around if time exceeds duration
        
        # Calculate the index in the angles array
        angles = self.angles[self.active_gait]
        index = int(time / (gait.duration / len(angles)))
        _angles = angles[index]
        
        #print('Angles at time {:.2f}: {}'.format(time, angles))
        
        # Set angles for each leg
        for i in range(len(self.legs)):
            leg = self.legs[i]
            if leg is not None:
                #print(f'Setting angles for leg {i} at time {time:.2f}: {angles[i]}')
                leg.set_angles(_angles[i])
