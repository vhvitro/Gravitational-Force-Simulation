import math
from .physics import calculate_attraction
from .config_load import config

# Load configurations
constants = config.load_constants()
colors = config.load_colors()
display_settings = config.load_display_settings()

# Constants from JSON
G = constants['gravitational_constant']
ABSORPTION_COEFF = constants['absorption_coefficient']

# Display settings
WINDOW_WIDTH = display_settings['window']['width']
WINDOW_HEIGHT = display_settings['window']['height']

# Colors as tuples
BLACK = tuple(colors['black'])

class Body:
    """Represents a celestial body in the gravitational simulation (formerly Bloco)"""
    
    def __init__(self, x, y, color, mass, radius, x_vel, y_vel):
        self.exists = True  # Changed from 'existe'
        self.x = x
        self.y = y
        self.color = color  # Changed from 'cor'
        self.mass = mass    # Changed from 'massa'
        self.radius = radius # Changed from 'raio'
        self.orbit = []
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.ax = 0  # Initialize acceleration
        self.ay = 0

    def update_position(self, bodies):
        total_fx = total_fy = 0
        for body in bodies:
            if body == self:
                continue
            
            fx, fy = calculate_attraction(self, body)
            total_fx += fx
            total_fy += fy
        
        self.ax = total_fx / self.mass
        self.ay = total_fy / self.mass

        self.x_vel += self.ax
        self.y_vel += self.ay

        self.x += self.x_vel 
        self.y += self.y_vel 

        self.orbit.append((self.x, self.y))

def create_body(x, y, color, mass, radius, x_vel, y_vel, body_list):
    """Factory function to create a new celestial body"""
    new_body = Body(x, y, color, mass, radius, x_vel, y_vel)
    body_list.append(new_body)
    return new_body

def delete_body(body, body_list):
    """Remove a body from the simulation"""
    if body in body_list:
        body_list.remove(body)

def consume_body(consumer, consumed):
    """Handle one body consuming another"""
    if consumed.mass < constants['collision_threshold']:
        consumer.mass += consumed.mass
    else:    
        consumer.mass += ABSORPTION_COEFF * consumed.mass
    consumed.exists = False