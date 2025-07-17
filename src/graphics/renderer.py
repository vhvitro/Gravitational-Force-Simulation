import pygame
import math
from ..core.config_load import config

# Load configurations
colors = config.load_colors()
display_settings = config.load_display_settings()

# Constants
WINDOW_WIDTH = display_settings['window']['width']
WINDOW_HEIGHT = display_settings['window']['height']
WHITE = tuple(colors['white'])

class Renderer:
    """Handles all drawing operations for the simulation"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
    
    def draw_celestial_body(self, body):
        """Draw a celestial body with its orbit trail and information"""
        screen_x = body.x + WINDOW_WIDTH/2
        screen_y = body.y + WINDOW_HEIGHT/2    

        # Draw orbit trail
        if len(body.orbit) > 2:
            updated_points = []
            for point in body.orbit:
                orbit_x, orbit_y = point
                orbit_x += WINDOW_WIDTH/2
                orbit_y += WINDOW_HEIGHT/2
                updated_points.append((orbit_x, orbit_y))
        
            pygame.draw.lines(self.screen, body.color, False, updated_points, 2)

        # Draw the body
        pygame.draw.circle(self.screen, body.color, (int(screen_x), int(screen_y)), body.radius)

        # Draw information text
        self._draw_body_info(body, screen_x, screen_y)
    
    def _draw_body_info(self, body, x, y):
        """Draw velocity, position, and acceleration information"""
        info_texts = [
            f"Vx={round(body.x_vel,2)}m/s",
            f"Vy={round(body.y_vel,2)}m/s",
            f"X={round(body.x,2)}m",
            f"Y={round(body.y,2)}m",
            f"Ax={round(body.ax,6)}m/s²",
            f"Ay={round(body.ay,6)}m/s²"
        ]
        
        for i, text in enumerate(info_texts):
            rendered_text = self.font.render(text, 1, WHITE)
            if i < 2:  # Velocity texts
                self.screen.blit(rendered_text, (x - rendered_text.get_width()*1.5, y - rendered_text.get_height()*(1.5 + i*2)))
            else:  # Position and acceleration texts
                offset_x = -0.5 if i < 4 else -1
                offset_y = -1.5 - (i-2)*2 if i < 4 else -2 - (i-4)*2
                self.screen.blit(rendered_text, (x - rendered_text.get_width()*offset_x, y - rendered_text.get_height()*offset_y))
    
    def draw_collision_counter(self, count):
        """Draw collision counter"""
        count_text = self.font.render(f"{count}", 1, WHITE)                
        self.screen.blit(count_text, (10, 10))