from servo_drivers.abstract import NetworkServoDriver
import socket as pysocket
import json

# Note: currently this driver will block the thread at program start until a client connects, then it will crash the program if the client disconnects.
class TCPNetworkServoDriver(NetworkServoDriver):
    
    def __init__(self, ip: str, port: int):
        
        server_sock = pysocket.socket(pysocket.AF_INET, pysocket.SOCK_STREAM)
        server_sock.setsockopt(pysocket.SOL_SOCKET, pysocket.SO_REUSEADDR, 1)
        server_sock.bind((ip, port))
        server_sock.listen(1)

        print(f"Waiting for TCP client on {ip}:{port}...")
        client_sock, addr = server_sock.accept()
        print(f"Accepted connection from {addr}")
        
        self.socket = client_sock

    def set_angle(self, address: list[int], angle: float):
        data = {"address": address, "angle": angle}
        self.socket.send(json.dumps(data).encode())
        print(f"Simulated PWM on ports {address}: angle={angle}")
        
    def kill(self):
        data = {"command": "kill"}
        self.socket.send(json.dumps(data).encode())
        print("Kill command sent")