from abc import ABC, abstractmethod

class ServoDriver(ABC):
    """Base class for any servo driver."""
    
    @abstractmethod
    def set_angle(self, address: list[int], angle: float):
        """Set the angle of the servo at the specified address."""
        pass
    
    @abstractmethod
    def kill(self):
        """Stop all servos."""
        pass
    
class NetworkServoDriver(ServoDriver):
    """Abstract class for network-based servo drivers."""
    
    
    def __init__(self, ip: str, port: int):
        """Initialize the network connection."""
        self.ip = ip
        self.port = port
        # Here you would typically set up the network connection
        # For example, using a socket or a specific protocol
        pass