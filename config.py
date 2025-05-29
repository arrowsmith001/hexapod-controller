from model.hexapod import Hexapod, HexapodLeg, HexapodLegJoint
from servo_drivers.abstract import ServoDriver

USE_NETWORK_DRIVER = True
driver = None | ServoDriver

if USE_NETWORK_DRIVER:
    from servo_drivers.tcp_network_servo_driver import TCPNetworkServoDriver
    driver = TCPNetworkServoDriver('0.0.0.0', 5555)
    # from servo_drivers.zmq_network_servo_driver import ZMQNetworkServoDriver
    # driver = ZMQNetworkServoDriver('localhost', 5555)
else:
    from servo_drivers.pi_hat_pwm_driver import PiHatPWMDriver
    driver = PiHatPWMDriver()
    
left_back_ports = [[1,13], [1,14], [1,15]]
left_mid_ports = [[0,4], [0,5], [0,6]]
left_front_ports = [[0,2], [0,1], [0,0]]

right_front_ports = [[0,10], [0,9], [0,8]]
right_mid_ports = [[1,9], [1,10], [1,11]]
right_back_ports = [[1,5], [1,6], [1,7]]

left_back_leg = HexapodLeg([-39.435, -61.125, -21.970], -135,
    HexapodLegJoint(driver, left_back_ports[0], angle_offset=-6), 
    HexapodLegJoint(driver, left_back_ports[1]), 
    HexapodLegJoint(driver, left_back_ports[2], invert=False, angle_offset=-18))
    
left_mid_leg = HexapodLeg([-49.4, 0.8, -21.970], -90,
    HexapodLegJoint(driver, left_mid_ports[0], angle_offset=-4), 
    HexapodLegJoint(driver, left_mid_ports[1]), 
    HexapodLegJoint(driver, left_mid_ports[2], angle_offset=-18))

left_front_leg = HexapodLeg([-39.435, 61.125, -21.970], -45,
    HexapodLegJoint(driver, left_front_ports[0], angle_offset=-10), 
    HexapodLegJoint(driver, left_front_ports[1]), 
    HexapodLegJoint(driver, left_front_ports[2], angle_offset=4))

right_front_leg = HexapodLeg([39.435, 61.125, -21.970], 45,
    HexapodLegJoint(driver, right_front_ports[0], invert=True, angle_offset=12), 
    HexapodLegJoint(driver, right_front_ports[1], invert=True), 
    HexapodLegJoint(driver, right_front_ports[2], invert=True, angle_offset=12), )

right_mid_leg = HexapodLeg([49.4, 0.8, -21.970], 90,
    HexapodLegJoint(driver, right_mid_ports[0], invert=True, angle_offset=6), 
    HexapodLegJoint(driver, right_mid_ports[1], invert=True), 
    HexapodLegJoint(driver, right_mid_ports[2], invert=True, angle_offset=8))

right_back_leg = HexapodLeg([39.435, -61.125, -21.970], 135,
    HexapodLegJoint(driver, right_back_ports[0], invert=True, angle_offset=6), 
    HexapodLegJoint(driver, right_back_ports[1], invert=True), 
    HexapodLegJoint(driver, right_back_ports[2], invert=True, angle_offset=18))

hexapod = Hexapod([left_front_leg, left_back_leg, right_front_leg, right_back_leg, left_mid_leg, right_mid_leg])