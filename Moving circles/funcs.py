import numpy as np 
import pygame 
import time

def update_body2_coords(body2, body1, FPS,rotation_angle,angular_velocity, distance):
    if rotation_angle >= 2 * np.pi:
        rotation_angle -= 2 * np.pi
    rotation_angle +=  angular_velocity

    body2['pos'][0] = body1['pos'][0] + distance * np.cos(rotation_angle)
    body2['pos'][1] =  body1['pos'][1] - distance * np.sin(rotation_angle)   
    
    return [body2['pos'][0], body2['pos'][1], rotation_angle]



def change_body_distance(body_x, body_y, rotation_angle,distance_change,grow):
    if not grow:
            body_x += (distance_change/2) * np.cos(rotation_angle)
            body_y -= (distance_change/2) * np.sin(rotation_angle)
    else:
            body_x -= (distance_change/2) * np.cos(rotation_angle)
            body_y += (distance_change/2) * np.sin(rotation_angle)
        
    return [body_x, body_y]

def get_rotation_angle_for_body2(rotation_angle):

    if rotation_angle <= np.pi:
        return rotation_angle + np.pi
    
    return rotation_angle - np.pi

def get_barycenter(body1, body2):
    masses = np.array([body1['mass'], body2['mass']])
    masses_sum = np.sum([body1['mass'],body2['mass']])
    bodies_x = np.array([body1['pos'][0],body2['pos'][0]])
    bodies_y = np.array([body1['pos'][1],body2['pos'][1]])
    
    bary_x = np.dot(bodies_x, masses)/masses_sum
    bary_y = np.dot(bodies_y, masses)/masses_sum
    return bari_x, bari_y