from model.hexapod import Hexapod, HexapodLeg, HexapodLegJoint
from servo_drivers.abstract import ServoDriver

USE_NETWORK_DRIVER = False
USE_ZMQ = False

def get_driver() -> ServoDriver:
    if USE_NETWORK_DRIVER:
        if USE_ZMQ:
            from servo_drivers.zmq_network_servo_driver import ZMQNetworkServoDriver
            return ZMQNetworkServoDriver('localhost', 5555)
        else:
            from servo_drivers.tcp_network_servo_driver import TCPNetworkServoDriver
            return TCPNetworkServoDriver('localhost', 5555)
    else:
        from servo_drivers.pi_hat_pwm_driver import PiHatPWMDriver
        return PiHatPWMDriver()

driver = get_driver()

# Port config
left_back_ports = [[1,14], [1,15],[1,13] ,]
left_mid_ports = [[0,4], [0,5], [0,6]]
left_front_ports = [[0,2], [0,1], [0,0]]

right_front_ports = [[0,10], [0,9], [0,8]]
right_mid_ports = [[1,9], [1,10], [1,11]]
right_back_ports = [[1,5], [1,7],[1,6], ]

# Resting angles (i.e. the angles of each leg segment to its joining leg when joint angles are set to zero)
femur_resting_angle = 14.795
tibia_resting_angle = 49.168

# Standing position
standing_x = 130
standing_y = 106
standing_z = -75
mid_standing_x = 152

# Crouching position
crouching_x = 75
crouching_y = 93
crouching_z = -25
mid_crouching_x = 90

x = crouching_x
y = crouching_y
z = crouching_z
mid_x = mid_crouching_x

left_back_leg = HexapodLeg([-39.435, -61.125, -21.970], [-x, -y, z],
    HexapodLegJoint(driver, left_back_ports[0],invert=False, angle_nudge=-4), 
    HexapodLegJoint(driver, left_back_ports[1],invert=True, angle_nudge=4), 
    HexapodLegJoint(driver, left_back_ports[2], invert=False, angle_nudge=4),
    [-135, femur_resting_angle, tibia_resting_angle])
    
left_mid_leg = HexapodLeg([-49.4, 0.8, -21.970], [-mid_x, 0, z],
    HexapodLegJoint(driver, left_mid_ports[0],invert=False, angle_nudge=-2), 
    HexapodLegJoint(driver, left_mid_ports[1],invert=True, angle_nudge=10), 
    HexapodLegJoint(driver, left_mid_ports[2], invert=False, angle_nudge=5),
    [-90, femur_resting_angle, tibia_resting_angle])

left_front_leg = HexapodLeg([-39.435, 61.125, -21.970], [-x, y, z],
    HexapodLegJoint(driver, left_front_ports[0], invert=False ,angle_nudge=-8), 
    HexapodLegJoint(driver, left_front_ports[1],invert=True,angle_nudge=-4), 
    HexapodLegJoint(driver, left_front_ports[2], invert=False, angle_nudge=12),
    [-45, femur_resting_angle, tibia_resting_angle])

right_front_leg = HexapodLeg([39.435, 61.125, -21.970], [x, y, z],
    HexapodLegJoint(driver, right_front_ports[0], invert=False, angle_nudge=18), 
    HexapodLegJoint(driver, right_front_ports[1], invert=False, angle_nudge=-16), 
    HexapodLegJoint(driver, right_front_ports[2], invert=True, angle_nudge=-16),
    [45, femur_resting_angle, tibia_resting_angle])

right_mid_leg = HexapodLeg([49.4, 0.8, -21.970], [mid_x, 0 , z],
    HexapodLegJoint(driver, right_mid_ports[0], invert=False, angle_nudge=5
    ), 
    HexapodLegJoint(driver, right_mid_ports[1], invert=False, angle_nudge=-6), 
    HexapodLegJoint(driver, right_mid_ports[2], invert=True, angle_nudge=-12),
    [90, femur_resting_angle, tibia_resting_angle])

right_back_leg = HexapodLeg([39.435, -61.125, -21.970], [x, -y, z],
    HexapodLegJoint(driver, right_back_ports[0], invert=False, angle_nudge=6), 
    HexapodLegJoint(driver, right_back_ports[1], invert=False, angle_nudge=-10), 
    HexapodLegJoint(driver, right_back_ports[2], invert=True, angle_nudge=-4),
    [135, femur_resting_angle, tibia_resting_angle])

hexapod = Hexapod([
    left_front_leg, left_back_leg, right_front_leg, right_back_leg, left_mid_leg, right_mid_leg
    ])