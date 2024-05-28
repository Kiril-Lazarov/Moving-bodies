import numpy as np


class LightSignal:
    def __init__(self,origin_position, message, radius=0):
        self.origin_position = origin_position
        self.message = message
        self.radius = radius
        self.rect = [self.origin_position[0] - self.radius, self.origin_position[1] - self.radius,
                     2 * self.radius, 2 * self.radius]
        
    def update_signal_position(self, displacement_per_frame):    
        self.radius += displacement_per_frame
        self.rect = [self.origin_position[0] - self.radius, self.origin_position[1] - self.radius,
                     2 * self.radius, 2 * self.radius]

        
    @classmethod
    def create_signal(cls, origin_position, message):
        return cls(origin_position, message)