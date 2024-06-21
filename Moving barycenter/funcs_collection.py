import numpy as np 
import pygame
import time

from circle import Circle


def get_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

'''
Initialization of the positions and distances to the center of rotation 
of the rotating bodies. The bodies are arranged at equal angular intervals 
starting from zero degrees. The angular intervals are equal to 360 degrees 
divided by the number of bodies participating in the rotation. The distances 
to the center decrease with each subsequently initialized body.
'''
def create_moving_circles(screen_center, Circle, count, 
                          unit_angle, mass, distance, 
                          color, rotating_circles_radius,center_point_radius):
    unit_distance = distance / (count/2)
    circles = []
    opposite_circles = []
    for i in range(int(count/2)):
        angle = i * unit_angle
        opposite_angle = angle + np.pi
       
        curr_circle_distance = distance - i * unit_distance
        distance_to_opp_point = curr_circle_distance - distance + rotating_circles_radius + center_point_radius
      
        
        circle_coords = (screen_center[0] + curr_circle_distance* np.cos(angle), 
                          screen_center[1] - curr_circle_distance*np.sin(angle))
        
        opposite_coords = (screen_center[0] + distance_to_opp_point* np.cos(opposite_angle), 
                          screen_center[1] - distance_to_opp_point*np.sin(opposite_angle))
        
        circles.append(Circle(*circle_coords, mass,curr_circle_distance, 
                              color, rotating_circles_radius, angle,))
        
        opposite_circles.append(Circle(*opposite_coords, mass, abs(distance_to_opp_point), 
                                       color,rotating_circles_radius, opposite_angle))
    return circles + opposite_circles



'''
Calculation of the center of mass of a given number of bodies based on their positions and masses
'''
def calc_barycenter(bodies, platform_point):
    
    # Add platform point to the bodies list
    all_bodies = bodies.copy()
    all_bodies.append(platform_point)
    
    masses = []
    x = []
    y = []
    
    for i in range(len(all_bodies)):
        body = all_bodies[i]
        x.append(body.x)
        y.append(body.y)
        masses.append(body.mass)
        
        
    masses = np.array(masses)
    masses_sum = np.sum(masses)
    bodies_x = np.array(x)
    bodies_y = np.array(y)
    
    bary_x = np.dot(bodies_x, masses)/masses_sum
    bary_y = np.dot(bodies_y, masses)/masses_sum
    
    return bary_x, bary_y


''' 
Updating the coordinates of rotating bodies. By default, 
this is done relative to their center of rotation, but it can
also be done relative to their center of mass.
'''
def update_circles_coords(circles_list, unit_displace, delta_angle,refference_point,to='platform_center_point'):

    for circle in circles_list:
       
        circle.change_angle(delta_angle)
        circle.change_distance(unit_displace)
        
        circle.set_coords(refference_point, to=to)
        
'''
Calculates the magnitude of the displacement for each frame of each body according to the ratios of their masses.
'''
def calc_displacements(circle_mass, platform_mass, unit_displace):
    min_displacement = unit_displace/ (circle_mass + platform_mass)
    
    circle_displacement = min_displacement * platform_mass
    platform_displacement = min_displacement * circle_mass
    
    return circle_displacement, platform_displacement

def get_angle_between_points(point1, point2):
    
    tangens = abs(point2[1]-point1[1])/abs(point2[0] - point1[0])
    
    angle = np.arctan(tangens)
    
    final_angle = np.pi + angle
    
    return final_angle

'''
Calculates the position of the platform point - the center of rotation - 
relative to each of the rotating bodies. Returns a numpy array with these coordinates.
'''
def calc_fictitious_platform_point(circles_list,platform_point,circle_displacement,platform_displacement):
    fictitious_platform_point_coords = []
    for circle in circles_list:
        circle.change_distance(circle_displacement)
        circle.set_coords([platform_point.x, platform_point.y])
        current_angle = circle.angle
        if  circle.angle >= np.pi:
            current_angle -= np.pi
            
        fict_platform_x = platform_point.x + platform_displacement * np.cos(current_angle)
        fict_platform_y = platform_point.y - platform_displacement *np.sin(current_angle)

        fictitious_platform_point_coords.append([fict_platform_x, fict_platform_y])

    return np.array(fictitious_platform_point_coords)

'''
Calculates the new position of the platform point as the average of the fictitious 
positions returned by calc_fictitious_platform_point, then recalculates the coordinates 
of the rotating bodies based on this new position and the distances of the bodies 
relative to the center of rotation.
'''
def calc_new_circles_positions(circles_list,platform_point,fictitious_platform_point_coords,platform_displacement):
    platform_point.x = fictitious_platform_point_coords[:,0].mean()
    platform_point.y = fictitious_platform_point_coords[:,1].mean()
    
    for circle in circles_list:
        circle.change_distance(platform_displacement)
        circle.set_coords([platform_point.x, platform_point.y])

def main_anim(rotating_circles_number, 
              platform_mass,
              circle_mass,
              distance,
              screen_width=1500, screen_height=800):
    
    if rotating_circles_number % 2 != 0:
        raise ValueError('Rotating bodies cannot be an odd number')
    # screen_center = (screen_width / 2, screen_height / 2)
    screen_center = (20, screen_height / 2)
    
    FPS = 100
    '''
    Initializations
    '''
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
  
    # platform_mass = 40
    platform_color = (0, 0, 0)
    platform_point_radius = 2
    
    
    platform_point = Circle(screen_center[0], screen_center[1], 
                            platform_mass, 0, platform_color, platform_point_radius,
                            np.pi)

    '''
    Local variables
    '''
    # rotating_circles_count = 4
    unit_angle = 2 * np.pi / rotating_circles_number
    delta_angle = 2 * np.pi / (FPS * 4)
    
    # circle_mass = 1
    color = (0, 0, 255)
    rotating_circles_radius = 4
    center_point_radius = 1
    distance -= center_point_radius - rotating_circles_radius # In pixels
    unit_displace = (distance-10)/ (FPS * 2)
    
    circle_displacement, platform_displacement = calc_displacements(circle_mass, platform_mass,unit_displace)
    
    
    circles_list = create_moving_circles(screen_center, Circle,
                                         rotating_circles_number,
                                         unit_angle, circle_mass, distance,
                                         color, rotating_circles_radius,
                                         center_point_radius)
    
    barycenter_point = calc_barycenter(circles_list, platform_point)
    
    # Reinitialization of the angle and the distance between platform point and barycenter point
    # platform_point.angle = get_angle_between_points((platform_point.x, platform_point.y), barycenter_point)
    platform_point.distance = get_distance((platform_point.x, platform_point.y), barycenter_point)
    
    # Draw circles
    for curr_circle in circles_list:
        pygame.draw.circle(screen, (255, 0, 255), (curr_circle.x, curr_circle.y), curr_circle.radius)
    
    running = True
    
    while running:
        
        clock.tick(FPS)
        screen.fill((255, 255, 255))  # Clear the screen for each frame
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
          
        
        # update_circles_coords(circles_list, unit_displace, delta_angle,[platform_point.x, platform_point.y])
        
        # Rotate the circles over barycenter point with no change of the distances to it
        update_circles_coords(circles_list + [platform_point], 0, delta_angle,barycenter_point,to='barycenter_point')
        platform_point.change_angle(delta_angle)
        
        fictitious_platform_point_coords = calc_fictitious_platform_point(circles_list,
                                                                            platform_point,circle_displacement,
                                                                            platform_displacement)
        
        # Calculating the new coordinates of rotating bodies relative to the platform point. 
        calc_new_circles_positions(circles_list,platform_point,fictitious_platform_point_coords,platform_displacement)
        
        barycenter_point = calc_barycenter(circles_list, platform_point)
        
        # Draw barycenter
        pygame.draw.circle(screen, platform_point.color,
                           (barycenter_point[0], barycenter_point[1]),
                           platform_point.radius)
      
        #Draw center point
        pygame.draw.circle(screen, (255, 0, 0), (platform_point.x, platform_point.y), platform_point.radius)
        
        # Draw circles
        for curr_circle in circles_list:
            pygame.draw.circle(screen, (255, 0, 255), (curr_circle.x, curr_circle.y), curr_circle.radius)
           
        pygame.display.update()
        # time.sleep(0.1)
    
    pygame.quit()