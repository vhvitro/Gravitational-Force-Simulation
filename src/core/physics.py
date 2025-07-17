import math
from core.config_load import config

# Load constants
constants = config.load_constants()['physics']
colors = config.load_colors()

G = constants['gravitational_constant']
ABSORPTION_COEFF = constants['absorption_coefficient']
BLACK_HOLE_MASS = constants['black_hole_mass']
MASS_RATIO_THRESHOLD = constants['mass_ratio_threshold']
AU = constants['AU']
SCALE = 200/AU

BLACK = tuple(colors['black'])

# Global list for new bodies (equivalent to novos_blocos0)
new_bodies_queue = []

def create_body(x, y, color, mass, radius, x_vel, y_vel, body_list):
    """Factory function to create a new celestial body - moved here to avoid circular import"""
    from core.objects import Body
    new_body = Body(x, y, color, mass, radius, x_vel, y_vel)
    body_list.append(new_body)
    return new_body

def consume_body(consumer, consumed):
    """Handle one body consuming another - moved here to avoid circular import"""
    if consumed.mass < constants['collision_threshold']:
        consumer.mass += consumed.mass
    else:    
        consumer.mass += ABSORPTION_COEFF * consumed.mass
    consumed.exists = False

def calculate_attraction(body1, body2):
    """Calculate gravitational attraction between two bodies"""
    critical_distance = abs(body1.radius + body2.radius)
    distance_x = abs(body1.x - body2.x)
    distance_y = abs(body1.y - body2.y)
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    if distance <= critical_distance:
        # Handle collision/merging
        if body2.mass >= BLACK_HOLE_MASS and body1.mass >= BLACK_HOLE_MASS:
            # Both are black holes - merge them
            body2.exists = False
            body1.exists = False
            merged_x = (body1.x + body2.x) / 2
            merged_y = (body1.y + body2.y) / 2
            merged_mass = body1.mass + body2.mass
            merged_radius = (body1.radius + body2.radius) / 2
            create_body(merged_x, merged_y, BLACK, merged_mass, 
                       merged_radius, 0, 0, new_bodies_queue)

        elif body1.mass > MASS_RATIO_THRESHOLD * body2.mass:
            # body1 consumes body2
            if body2.mass >= constants['collision_threshold']:
                consume_body(body1, body2)
                # Create debris
                escape_velocity = 1.2 * math.sqrt(G * body1.mass / (body1.radius + body2.radius))
                create_body(body2.x, body2.y, body2.color, 
                           body2.mass * (1 - ABSORPTION_COEFF),
                           body2.radius / (1 + ABSORPTION_COEFF),
                           escape_velocity, escape_velocity, new_bodies_queue)
            else: 
                consume_body(body1, body2)
                
        elif body2.mass > body1.mass * MASS_RATIO_THRESHOLD:
            # body2 consumes body1
            if body1.mass >= constants['collision_threshold']:
                consume_body(body2, body1)
                escape_velocity = 1.2 * math.sqrt(G * body2.mass / (body1.radius + body2.radius))
                create_body(body1.x, body1.y, body1.color,
                           body1.mass * (1 - ABSORPTION_COEFF),
                           body1.radius / (1 + ABSORPTION_COEFF),
                           escape_velocity, escape_velocity, new_bodies_queue)
            else: 
                consume_body(body2, body1)
        
        # Return zero forces for collision cases
        return 0, 0
    
    else:
        # Calculate gravitational force
        F = G * body1.mass * body2.mass / distance**2
        theta = math.atan2(distance_y, distance_x)

        # Handle force direction components
        if body1.x < body2.x:
            F_x = math.cos(theta) * F
        else:
            F_x = math.cos(theta) * -F 
            
        if body1.y < body2.y:
            F_y = math.sin(theta) * F
        else:
            F_y = math.sin(theta) * -F 
            
        return F_x, F_y

def handle_collision(body1, body2):
    """Handle elastic collision between two bodies"""
    critical_distance = abs(body1.radius + body2.radius)/SCALE
    distance_x = abs(body1.x - body2.x)
    distance_y = abs(body1.y - body2.y)
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    if distance <= critical_distance:
        # Calculate relative velocities
        if (body1.x_vel < 0 and body2.x_vel < 0) or (body1.x_vel > 0 and body2.x_vel > 0):
            vrel_x = body1.x_vel + body2.x_vel
        else:
            vrel_x = body1.x_vel - body2.x_vel

        if (body1.y_vel < 0 and body2.y_vel < 0) or (body1.y_vel > 0 and body2.y_vel > 0):
            vrel_y = body1.y_vel + body2.y_vel
        else:
            vrel_y = body1.y_vel - body2.y_vel
            
        # Store original velocities
        xvel1, xvel2 = body1.x_vel, body2.x_vel
        yvel1, yvel2 = body1.y_vel, body2.y_vel
        
        # Determine restitution coefficient based on mass ratio
        if body1.mass >= 10 * body2.mass or body2.mass >= body1.mass * 10:
            e = 0  # Perfectly inelastic
        else:
            e = 1  # Perfectly elastic
            
        # Apply collision physics
        body1.x_vel = (body1.mass * xvel1 + body2.mass * xvel2 - body2.mass * vrel_x * e) / (body1.mass + body2.mass)
        body2.x_vel = vrel_x * e - abs(body1.x_vel)

        body1.y_vel = (body1.mass * yvel1 + body2.mass * yvel2 - body2.mass * vrel_y * e) / (body1.mass + body2.mass)
        body2.y_vel = vrel_y * e - abs(body1.y_vel)
        
        return True
    
    return False