import math
from enum import Enum
import numpy as np
from leg_position import LegPosition
from model.hexapod_leg import HexapodLeg
from model.hexapod_leg_joint import HexapodLegJoint
from motion import BezierMotion, Gait, LinearMotion, Motion
from servo_drivers.abstract import ServoDriver
from utils.servo import *
from constants import *
from utils.ik import trajectory_as_angles
    

class Hexapod:

    def __init__(self, legs : list[HexapodLeg]):
        # For each leg, its position is deduced. 
        # The hexapods surrounding area is divided into 6 equal sections. Then the angle is read to determine the leg's position.
        self.legs: list[HexapodLeg | None] = [None] * 6
        for i in range(len(legs)):
            leg: HexapodLeg = legs[i]
            heading = leg.heading
            position = None or LegPosition
            if heading > -180 and heading < 0:
                # Left side legs
                if heading < -120:
                    position = LegPosition.LEFT_BACK
                elif heading < -60:
                    position = LegPosition.LEFT_MID
                else:
                    position = LegPosition.LEFT_FRONT
            elif heading >= 0 and heading < 180:
                # Right side legs
                if heading < 60:
                    position = LegPosition.RIGHT_FRONT
                elif heading < 120:
                    position = LegPosition.RIGHT_MID
                else:
                    position = LegPosition.RIGHT_BACK
            else:
                raise ValueError("Invalid leg heading: " + str(heading))
            if self.legs[position.value] is not None:
                conflicting_leg = self.legs[position.value]
                conflict_heading = conflicting_leg.heading if conflicting_leg is not None else None
                raise ValueError("Duplicate leg heading: " + str(heading) + " conflicts with " + str(conflict_heading))
            self.legs[position.value] = leg
            leg.set_initial_angles()
            
    def set_gait(self, gait: Gait):
        self.gait = gait
            
    def get_leg(self, position: LegPosition):
        if position.value < 0 or position.value >= len(self.legs):
            raise ValueError("Invalid leg position")
        return self.legs[position.value]
    
    def compute_joint_angles(self, delta=0.5):
        print("Computing joint angles for gait with duration:", self.gait.duration)
        if not hasattr(self, 'gait'):
            raise ValueError("Gait not set")
        
        self.angles = []
        
        # Pre-fill array with zeroes
        for i in range(int(self.gait.duration / delta) + 1):
            self.angles.append([[0,0,0]] * 6)
            
        # One leg at a time in time order (since the absolute position needs to be calculated)
        for i in range(len(self.legs)):
            leg = self.legs[i]
            if leg is None:
                continue
            
            ordered_leg_motions: list[Motion] = self.gait.get_leg_motions_in_time_order(LegPosition(i))
            
            # Start with the initial angles for this leg
            initial_angles = leg.get_angles()
            steps = int(self.gait.duration / delta) + 1
            leg_angles = [initial_angles]
            current_pos = leg.get_foot_position()

            # Build the full trajectory for this leg by stitching together all motions
            current_time = 0.0
            for motion in ordered_leg_motions:
                # Determine start and end time for this motion
                start_time = max(current_time, motion.start)
                end_time = min(self.gait.duration, motion.duration + motion.start)
                steps = int((end_time - start_time) / delta)
                if steps <= 0:
                    continue
                # Calculate target position
                target_pos = np.array(current_pos) + np.array(motion.vector)
                traj = trajectory_as_angles(current_pos, target_pos, steps, leg.heading, motion.control_point if isinstance(motion, BezierMotion) else None)
                leg_angles.extend(traj[1:])  # skip the first, already included
                current_time = end_time

            # If the trajectory is shorter than the total time, pad with last known angles
            while len(leg_angles) < steps:
                leg_angles.append(leg_angles[-1])

            # Assign the computed angles to the main angles array
            for idx in range(steps):
                self.angles[idx][i] = leg_angles[idx]
                
        print("Computed joint angles for " + str(len(self.angles)) + " steps.")
            
    def set_angles_at(self, time: float):
        if not hasattr(self, 'angles'):
            raise ValueError("Angles not computed. Call compute_joint_angles() first.")
        
        if time < 0 or time >= self.gait.duration:
            time = time % self.gait.duration  # Wrap around if time exceeds duration
        
        # Calculate the index in the angles array
        index = int(time / (self.gait.duration / len(self.angles)))
        angles = self.angles[index]
        
        # Set angles for each leg
        for i in range(len(self.legs)):
            leg = self.legs[i]
            if leg is not None:
                leg.set_angles(angles[i])
