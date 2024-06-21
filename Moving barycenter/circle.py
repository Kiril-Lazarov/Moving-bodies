import numpy as np

class Circle:
    
   
    def __init__(self,x, y, mass, distance, color,radius, angle):
        self.x = x
        self.y = y
        self.mass = mass
        self.distance = distance
        self.color = color
        self.radius = radius
        self.angle = angle
          
    
    @staticmethod
    def get_distance(point1, point2):
        return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        
    def change_angle(self, angle):    
        self.angle += angle
        if self.angle >= 2 * np.pi:
            self.angle -= 2 * np.pi
            
            
    def set_coords(self, refference_point,to='platform_center_point'):
      
        distance = self.get_distance(refference_point, [self.x,self.y]) if to=='barycenter_point' else self.distance 
        self.x = refference_point[0] + distance * np.cos(self.angle)
        self.y = refference_point[1] - distance *np.sin(self.angle)
        
        
    def change_distance(self, displacement):
        
        if 0<= self.angle < np.pi:
            self.distance -= displacement
        else:
            self.distance += displacement