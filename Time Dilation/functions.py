import numpy as np 
import pygame 
from datetime import datetime

def create_background(screen_width, screen_height, bg_color, units, length):
    # Create background object
    background_surface = pygame.Surface((screen_width, screen_height))
    
    # Create font
    font_small = pygame.font.Font(None, 26)
    background_surface.fill(bg_color)
    
    markers = []
    
    # Coordinate x-line parameters
    x_line_start = screen_width-1400
    x_line_end = screen_width-100
    y_line = screen_height-150    
    line_color = (185, 185, 185)
    
    markers.append({
        'receiver_x': x_line_end,
        'receiver_y': y_line
    })
    
    pygame.draw.line(background_surface, color = line_color, start_pos=(x_line_start, y_line),
                         end_pos = (x_line_end, y_line), width=2)
        
   

    vertical_line_start = y_line - 10
    vertical_line_end = y_line + 10
    number_y = vertical_line_end + 15

    for i in range(units+1):
        vertical_line_x = x_line_start + i*length

        pygame.draw.line(background_surface, color = line_color, start_pos=(vertical_line_x, vertical_line_start),
                     end_pos = (vertical_line_x, vertical_line_end), width=1)

        number = font_small.render(f'{units-i}', True, line_color)
        background_surface.blit(number, (vertical_line_x-5,number_y))
        
    description = font_small.render(f'Distance in light seconds', True, line_color)
    background_surface.blit(description, (x_line_start+550, y_line+50))
    
    return background_surface, markers


def update_first_light_front(first_light_front, displacement_per_frame):
    first_light_front[0] += displacement_per_frame
    return first_light_front


def gamma_factor(v):
    return np.sqrt(1 - v ** 2)

# Update the coordinates of the messages emitted by the spaceship that are shown on the screen.
def update_message_position(vis_angle, signal):
    
    x = signal.origin_position[0] + signal.radius    
    y= signal.origin_position[1] - 50
    
    return x, y