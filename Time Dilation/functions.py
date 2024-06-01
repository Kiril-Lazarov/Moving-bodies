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
    
    '''New logic'''
    
    screen_objects = {
        'x_line_start': x_line_start,
        'vertical_line_start': vertical_line_start,
        'vertical_line_end': vertical_line_end,
        'x_line_end': x_line_end,
        'y_line': y_line,
        'vertical_line_x': [],
        'numbers': [],
        'signals_start_positions': [],
        'spaceship_position': []
    }
    '''New logic'''

    for i in range(units+1):
        vertical_line_x = x_line_start + i*length

        pygame.draw.line(background_surface, color = line_color, start_pos=(vertical_line_x, vertical_line_start),
                     end_pos = (vertical_line_x, vertical_line_end), width=1)
        
        '''New logic'''
        screen_objects['vertical_line_x'].append(vertical_line_x)
        '''New logic'''

        number = font_small.render(f'{units-i}', True, line_color)
        background_surface.blit(number, (vertical_line_x-5,number_y))
        
        '''New logic'''
        screen_objects['numbers'].append([units-i, vertical_line_x-5,number_y])
        '''New logic'''
        
    description = font_small.render(f'Distance in light seconds', True, line_color)
    background_surface.blit(description, (x_line_start+550, y_line+50))
    
    return background_surface, markers, screen_objects


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

# Update the dictionary containing the data of the received signals from the receiver
def update_readings(readings_dict, count, time, message):
    x_time = 1000
    x_message = 1250
    init_y = 35
    y_change = 30
    y_displace = init_y + count * y_change
    
    readings_dict[count] = {'time': [time, x_time, y_displace],
                            'message': [message, x_message, y_displace]}
    return readings_dict


def show_readings(readings_dict, font_big, win):
    for data in readings_dict.values():
        time_text = font_big.render(f'{data["time"][0]}', True, (0, 0, 0))
        message_text = font_big.render(f'{data["message"][0]}', True, (0, 0, 0))
        
        win.blit(time_text, (data["time"][1], data["time"][2]))
        win.blit(message_text, (data["message"][1], data["message"][2])) 