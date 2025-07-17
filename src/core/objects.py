import math
from core.config_load import config

# Load configurations
constants = config.load_constants()['physics']
simulation_constants = config.load_constants()['simulation']
colors = config.load_colors()
display_settings = config.load_display_settings()

# Constants from JSON
G = constants['gravitational_constant']
ABSORPTION_COEFF = constants['absorption_coefficient']
TIME_STEP = simulation_constants['time_step_per_frame']
FPS = simulation_constants['target_fps']
AU = constants['AU']
SCALE = 200/AU
MAX_ORBIT = math.sqrt(1/TIME_STEP) * 60**3

# Display settings
WINDOW_WIDTH = display_settings['window']['width']
WINDOW_HEIGHT = display_settings['window']['height']

# Colors as tuples
BLACK = tuple(colors['black'])

class Body:
    """Represents a celestial body in the gravitational simulation"""
    
    def __init__(self, x, y, color, mass, radius, x_vel, y_vel):
        self.exists = True
        self.x = x
        self.y = y
        self.color = color
        self.mass = mass
        self.radius = radius
        self.orbit = []
        self.x_vel = x_vel  # m/s
        self.y_vel = y_vel  # m/s
        self.ax = 0  # m/s²
        self.ay = 0  # m/s²
        
        # Orbit trail management
        self.orbit_update_counter = 0
        self.orbit_update_frequency = 10  # Update orbit every N frames
        
        # Debug: Print initial position
        print(f"Body created at ({x}, {y}) with mass {mass}")

    def update_position(self, bodies, time_step):
        """Update position using the fixed time step"""
        from core.physics import calculate_attraction
        
        # Store old position for debugging
        old_x, old_y = self.x, self.y
        
        # Calculate total gravitational forces
        total_fx = total_fy = 0
        for body in bodies:
            if body == self:
                continue
            
            fx, fy = calculate_attraction(self, body)
            total_fx += fx
            total_fy += fy
        
        # Calculate acceleration (F = ma -> a = F/m)
        self.ax = total_fx / self.mass
        self.ay = total_fy / self.mass

        # Update velocity: v = v + a * dt
        self.x_vel += self.ax * time_step
        self.y_vel += self.ay * time_step

        # Update position: x = x + v * dt
        self.x += self.x_vel * time_step
        self.y += self.y_vel * time_step

        # Debug: Print position changes every 60 frames
        if hasattr(self, 'debug_counter'):
            self.debug_counter += 1
        else:
            self.debug_counter = 0
            
        if self.debug_counter % 60 == 0:  # Every second at 60fps
            print(f"Body: pos=({self.x:.1f}, {self.y:.1f}), vel=({self.x_vel:.1f}, {self.y_vel:.1f}), acc=({self.ax:.6f}, {self.ay:.6f})")

        # Update orbit trail
        self.orbit.append((self.x*SCALE, self.y*SCALE))
        
        # Limit orbit trail length
        if len(self.orbit) > MAX_ORBIT:
            self.orbit.pop(0)

    def get_speed(self):
        """Get current speed in m/s"""
        return math.sqrt(self.x_vel**2 + self.y_vel**2)

def delete_body(body, body_list):
    """Remove a body from the simulation"""
    if body in body_list:
        body_list.remove(body)