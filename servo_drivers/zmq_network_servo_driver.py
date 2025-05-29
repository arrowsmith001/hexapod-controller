from servo_drivers.abstract import NetworkServoDriver
import zmq
    
class ZMQNetworkServoDriver(NetworkServoDriver):
    def __init__(self, ip: str, port: int):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://{ip}:{port}".format(ip=ip, port=port))
        self.socket = socket

    def set_angle(self, address: list[int], angle: float):
        # Send the angle over the provided socket
        self.socket.send_string(str("hello"))
        # response = self.socket.recv_string()
        print(f"Simulated PWM on ports {address}: angle={angle}")
        
    def kill(self):
        # Send a kill command over the socket
        self.socket.send_string("kill")
        response = self.socket.recv_string()
        print(f"Kill command sent, response: {response}")