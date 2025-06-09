from hexapod.leg_position import LegType
from hexapod.motion import Gait, LinearMotion, BezierMotion, Pause

# A Gait is defined by a set of Motions, each with a start time and duration

reach = 25
elevation = -40
control_height = 50

dur = 1
interval = 0.1 
m = 0.5 # control point lateral offset multiplier
delay = 0.75

stand = Gait([
    
    BezierMotion([-reach, reach, elevation], 0, dur, LegType.LEFT_FRONT, [-reach*m, reach*m, control_height]),
    #BezierMotion([reach, -reach, -elevation], dur, dur, LegType.LEFT_FRONT, [-reach*m, reach*m, control_height]),
    BezierMotion([-reach, -reach, elevation], 0, dur, LegType.LEFT_BACK, [-reach*m, -reach*m, control_height]),
    #BezierMotion([reach, reach, -elevation], dur, dur, LegType.LEFT_BACK, [-reach*m, -reach*m, control_height]),
    BezierMotion([reach, 0, elevation], 0, dur, LegType.RIGHT_MID, [reach*m, 0, control_height]),
    #BezierMotion([-reach, 0, -elevation], dur, dur, LegType.RIGHT_MID, [reach*m, 0, control_height]),
    
    BezierMotion([-reach, 0, elevation], delay, dur, LegType.LEFT_MID, [-reach*m, 0, control_height]),
    #BezierMotion([reach, 0, -elevation], dur + delay, dur, LegType.LEFT_MID, [-reach*m, 0, control_height]),
    BezierMotion([reach, reach, elevation], delay, dur, LegType.RIGHT_FRONT, [reach*m, reach*m, control_height]),
    #BezierMotion([-reach, -reach, -elevation], dur + delay, dur, LegType.RIGHT_FRONT, [reach*m, -reach*m, control_height]),
    BezierMotion([reach, -reach, elevation], delay, dur, LegType.RIGHT_BACK, [reach*m, -reach*m, control_height]),
    #BezierMotion([-reach, reach, -elevation], dur + delay, dur, LegType.RIGHT_BACK, [reach*m, -reach*m, control_height]),
    
    Pause(dur, 2, LegType.LEFT_FRONT),
    Pause(dur, 2, LegType.LEFT_BACK),
    Pause(dur, 2, LegType.RIGHT_MID),
    Pause(dur+delay, 2 - delay, LegType.LEFT_MID),
    Pause(dur+delay, 2- delay, LegType.RIGHT_FRONT),
    Pause(dur+delay, 2- delay, LegType.RIGHT_BACK),
])


dur = 1
stride_length = 45
stride_control_height = 50
elevation = -40

# Proper wave gait, when each leg is continuously in its stance phase when its not swinging
wave_gait_1 = Gait([
    
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    LinearMotion([0, -stride_length, 0], dur, 5*dur, LegType.LEFT_BACK),
    
    LinearMotion([0, -stride_length*0.2, 0], 0, dur, LegType.LEFT_MID),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    LinearMotion([0, -stride_length*0.8, 0], dur*2, 4*dur, LegType.LEFT_MID),
    
    LinearMotion([0, -stride_length*0.4, 0], 0, dur*2, LegType.LEFT_FRONT),
    BezierMotion([0, stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    LinearMotion([0, -stride_length*0.6, 0], dur*3, 3*dur, LegType.LEFT_FRONT),
    
    LinearMotion([0, -stride_length*0.6, 0], 0, dur*3, LegType.RIGHT_BACK),
    BezierMotion([0, stride_length, 0], dur*3, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    LinearMotion([0, -stride_length*0.6, 0], dur*4, 2*dur, LegType.RIGHT_BACK),
    
    LinearMotion([0, -stride_length*0.8, 0], 0, dur*4, LegType.RIGHT_MID),
    BezierMotion([0, stride_length, 0], dur*4, dur, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height]),
    LinearMotion([0, -stride_length*0.2, 0], dur*5, dur, LegType.RIGHT_MID),
    
    LinearMotion([0, -stride_length, 0], 0, dur*5, LegType.RIGHT_FRONT),
    BezierMotion([0, stride_length, 0], dur*5, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
])

# Wave gait variant where swings are done first, then all strides are done at once
wave_gait_2 = Gait([
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*3, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*4, dur, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*5, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.LEFT_BACK),
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.LEFT_MID),
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.LEFT_FRONT),
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.RIGHT_MID),
    LinearMotion([0, -stride_length, 0], dur*6, dur, LegType.RIGHT_FRONT),
])

dur = 0.25
stride_length = 45
stride_control_height = 40
elevation = -40

# Ripple gait - because there is overlapping motion, we need an initial phase and continuous phase which differ by one motion
ripple_gait_init = Gait([
    #BezierMotion([0, stride_length, 0], 0, dur*0.5, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height], t_start=0.5),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*0.5, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*1.5, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2.5, dur*0.5, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height], t_end=0.5),
    
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_BACK),
    
    LinearMotion([0, -stride_length*(1.0/4), 0], 0, dur*0.5, LegType.RIGHT_FRONT),
    LinearMotion([0, -stride_length*(3.0/4), 0], dur*1.5, dur*1.5, LegType.RIGHT_FRONT),
    
    LinearMotion([0, -stride_length*(2.0/4), 0], 0, dur, LegType.LEFT_MID),
    LinearMotion([0, -stride_length*(2.0/4), 0], dur*2, dur, LegType.LEFT_MID),
    
    LinearMotion([0, -stride_length*(3.0/4), 0], 0, dur*1.5, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length*(1.0/4), 0], 0, dur*1.5, LegType.RIGHT_BACK),
    
    LinearMotion([0, -stride_length, 0], 0, dur*2, LegType.LEFT_FRONT),
    
    LinearMotion([0, -stride_length, 0], 0, dur*2.5, LegType.RIGHT_MID)
])

ripple_gait = Gait([
    BezierMotion([0, stride_length, 0], 0, dur*0.5, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height], t_start=0.5),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*0.5, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*1.5, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2.5, dur*0.5, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height], t_end=0.5),
    

    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_BACK),
    
    LinearMotion([0, -stride_length*(1.0/4), 0], 0, dur*0.5, LegType.RIGHT_FRONT),
    LinearMotion([0, -stride_length*(3.0/4), 0], dur*1.5, dur*1.5, LegType.RIGHT_FRONT),
    
    LinearMotion([0, -stride_length*(2.0/4), 0], 0, dur, LegType.LEFT_MID),
    LinearMotion([0, -stride_length*(2.0/4), 0], dur*2, dur, LegType.LEFT_MID),
    
    LinearMotion([0, -stride_length*(3.0/4), 0], 0, dur*1.5, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length*(1.0/4), 0], 0, dur*1.5, LegType.RIGHT_BACK),
    
    LinearMotion([0, -stride_length, 0], 0, dur*2, LegType.LEFT_FRONT),
    
    LinearMotion([0, -stride_length, 0], dur*0.5, dur*2.5, LegType.RIGHT_MID)
])

dur = 0.2
stride_length = 30
stride_control_height = 60

tripod_gait = Gait([
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_BACK),
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_FRONT),
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.RIGHT_MID),
    LinearMotion([0, -stride_length, 0], 0, dur, LegType.LEFT_MID),
    LinearMotion([0, -stride_length, 0], 0, dur, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length, 0], 0, dur, LegType.RIGHT_FRONT),
])

# Any forward gait can be turned into a left or right turn by changing the direction of the leg on one side
tripod_left_turn = Gait([
    BezierMotion([0, -stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], 0, dur, LegType.LEFT_FRONT, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur, dur, LegType.LEFT_MID, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    
    LinearMotion([0, stride_length, 0], dur, dur*2, LegType.LEFT_BACK),
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.RIGHT_MID),
    LinearMotion([0, stride_length, 0], dur, dur*2, LegType.LEFT_FRONT),
    LinearMotion([0, stride_length, 0], 0, dur, LegType.LEFT_MID),
    LinearMotion([0, -stride_length, 0], 0, dur, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length, 0], 0, dur, LegType.RIGHT_FRONT),
])

tripod_right_turn = Gait([
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], 0, dur, LegType.RIGHT_MID, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur, dur, LegType.RIGHT_BACK, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur, dur, LegType.RIGHT_FRONT, [0, -stride_length/2, stride_control_height]),
    
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_BACK),
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_MID),
    LinearMotion([0, -stride_length, 0], dur, dur*2, LegType.LEFT_FRONT),
    LinearMotion([0, stride_length, 0], 0, dur, LegType.RIGHT_BACK),
    LinearMotion([0, stride_length, 0], 0, dur, LegType.RIGHT_MID),
    LinearMotion([0, stride_length, 0], 0, dur, LegType.RIGHT_FRONT),
])

ripple_left_turn = Gait([
    BezierMotion([0, -stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*0.5, dur, LegType.RIGHT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur, dur, LegType.LEFT_MID, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*1.5, dur, LegType.RIGHT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2.5, dur, LegType.RIGHT_MID, [0, stride_length/2, stride_control_height]),
    
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.LEFT_BACK),
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.RIGHT_FRONT),
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.LEFT_MID),
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.RIGHT_BACK),
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.LEFT_FRONT),
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.RIGHT_MID)
])

ripple_right_turn = Gait([
    BezierMotion([0, stride_length, 0], 0, dur, LegType.LEFT_BACK, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur*0.5, dur, LegType.RIGHT_FRONT, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur, dur, LegType.LEFT_MID, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur*1.5, dur, LegType.RIGHT_BACK, [0, -stride_length/2, stride_control_height]),
    BezierMotion([0, stride_length, 0], dur*2, dur, LegType.LEFT_FRONT, [0, stride_length/2, stride_control_height]),
    BezierMotion([0, -stride_length, 0], dur*2.5, dur, LegType.RIGHT_MID, [0, -stride_length/2, stride_control_height]),
    
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.LEFT_BACK),
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.RIGHT_FRONT),
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.LEFT_MID),
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.RIGHT_BACK),
    LinearMotion([0, -stride_length, 0], 0, dur*3, LegType.LEFT_FRONT),
    LinearMotion([0, stride_length, 0], 0, dur*3, LegType.RIGHT_MID)
])

descent = 50
elevation = 40

dur = 0.25
across = 15

bob = Gait([
    LinearMotion([0, 0, -across/2], 0, dur, LegType.LEFT_BACK),
    LinearMotion([-0, 0, -across/2], 0, dur, LegType.LEFT_MID),
    LinearMotion([-0, 0, -across/2], 0, dur, LegType.LEFT_FRONT),
    LinearMotion([-0, 0, -across/2], 0, dur, LegType.RIGHT_BACK),
    LinearMotion([-0, 0, -across/2], 0, dur, LegType.RIGHT_MID),
    LinearMotion([-0, 0, -across/2], 0, dur, LegType.RIGHT_FRONT),
    LinearMotion([-across, 0, 0], dur, dur, LegType.LEFT_BACK),
    LinearMotion([-across, 0, 0], dur, dur, LegType.LEFT_MID),
    LinearMotion([-across, 0, 0], dur, dur, LegType.LEFT_FRONT),
    LinearMotion([-across, 0, 0], dur, dur, LegType.RIGHT_BACK),
    LinearMotion([-across, 0, 0], dur, dur, LegType.RIGHT_MID),
    LinearMotion([-across, 0, 0], dur, dur, LegType.RIGHT_FRONT),
    LinearMotion([0, 0, across], dur*2, dur, LegType.LEFT_BACK),
    LinearMotion([-0, 0, across], dur*2, dur, LegType.LEFT_MID),
    LinearMotion([-0, 0, across], dur*2, dur, LegType.LEFT_FRONT),
    LinearMotion([-0, 0, across], dur*2, dur, LegType.RIGHT_BACK),
    LinearMotion([-0, 0, across], dur*2, dur, LegType.RIGHT_MID),
    LinearMotion([-0, 0, across], dur*2, dur, LegType.RIGHT_FRONT),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.LEFT_BACK),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.LEFT_MID),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.LEFT_FRONT),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.RIGHT_BACK),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.RIGHT_MID),
    LinearMotion([across*2, 0, 0], dur*3, dur, LegType.RIGHT_FRONT),
    LinearMotion([0, 0, -across/2], dur*4, dur, LegType.LEFT_BACK),
    LinearMotion([-0, 0, -across/2], dur*4, dur, LegType.LEFT_MID),
    LinearMotion([-0, 0, -across/2], dur*4, dur, LegType.LEFT_FRONT),
    LinearMotion([-0, 0, -across/2], dur*4, dur, LegType.RIGHT_BACK),
    LinearMotion([-0, 0, -across/2], dur*4, dur, LegType.RIGHT_MID),
    LinearMotion([-0, 0, -across/2], dur*4, dur, LegType.RIGHT_FRONT),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.LEFT_BACK),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.LEFT_MID),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.LEFT_FRONT),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.RIGHT_BACK),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.RIGHT_MID),
    LinearMotion([-across, 0, 0], dur*5, dur, LegType.RIGHT_FRONT),
])