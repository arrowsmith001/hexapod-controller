import math
from enum import Enum
import numpy as np
from hexapod.leg_position import LegType
from model.hexapod_leg import HexapodLeg
from model.hexapod_leg_joint import HexapodLegJoint
from hexapod.motion import BezierMotion, Gait, LinearMotion, Motion
from servo_drivers.abstract import ServoDriver
from utils.servo import *
from hexapod.constants import *
from utils.ik import trajectory_as_angles, leg_ik
    

class Hexapod:

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
            
    def set_gait(self, gait: Gait):
        self.gait = gait
            
    def get_leg(self, position: LegType):
        if position.value < 0 or position.value >= len(self.legs):
            raise ValueError("Invalid leg position")
        leg = self.legs[position.value]
        if leg is None:
            raise ValueError("Leg at position " + position.name + " is not set")
        return leg
    
    def compute_joint_angles(self, delta=0.5):
        
        if self.gait.duration <= 0:
            raise ValueError("Gait duration must be greater than 0")
        
        total_steps = int(self.gait.duration / delta)
        
        if not hasattr(self, 'gait'):
            raise ValueError("Gait not set")
        
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
            motion_count = self.gait.get_leg_motion_count(leg_type)
            
            current_angles = leg.starting_angles
            current_reference_pos = leg.get_foot_position_at_angles(current_angles)
            current_time = 0
            
            #print('Starting angles: ', current_angles, 'for leg:', leg_type.name)
            #print('Starting reference position:', current_reference_pos, 'for leg:', leg_type.name)
            #print('leg_ik check:', leg_ik(current_reference_pos - leg_origin, leg.joint_rest_headings), 'for leg: ', leg_type.name)
            
            for i in range(total_steps):
                
                if motion_count == 0:
                    # No motions for this leg, just use the initial angles
                    angles[i, leg_type.value, :] = leg.starting_angles
                    continue
                
                current_time = i * delta
                current_motion = self.gait.get_leg_motion_at_time(leg_type, current_time)
                
                if current_motion is None:
                    # No motion at this time, use the last known angles
                    angles[i, leg_type.value, :] = current_angles
                    ###print('No motion at time:', current_time, 'using last known angles:', current_angles, 'for leg:', leg_type.name)
                    continue
                
                # Calculate target position
                pos = current_motion.interp(current_reference_pos - leg_origin, current_time)
                
                # Calculate the angles for this position
                _angles = leg_ik(pos, leg.joint_rest_headings)  
                
                # print('i :', i, 'current_time:', current_time, 'pos + origin check:', pos + leg_origin)
                # Set angles
                angles[i, leg_type.value, :] = _angles
                
                current_angles = _angles
                
                # If motion is at its end, update reference position
                motion_end = current_motion.start + current_motion.duration
                #print('current_time:', current_time, 'motion_end:', motion_end)
                if current_time + delta >= motion_end:
                    current_reference_pos = pos + leg_origin
                    
        self.angles = angles
        
            
    def set_angles_at(self, time: float):
        if not hasattr(self, 'angles'):
            raise ValueError("Angles not computed. Call compute_joint_angles() first.")
        
        if time < 0 or time >= self.gait.duration:
            time = time % self.gait.duration  # Wrap around if time exceeds duration
        
        # Calculate the index in the angles array
        index = int(time / (self.gait.duration / len(self.angles)))
        angles = self.angles[index]
        
        #print('Angles at time {:.2f}: {}'.format(time, angles))
        
        # Set angles for each leg
        for i in range(len(self.legs)):
            leg = self.legs[i]
            if leg is not None:
                #print(f'Setting angles for leg {i} at time {time:.2f}: {angles[i]}')
                leg.set_angles(angles[i])
