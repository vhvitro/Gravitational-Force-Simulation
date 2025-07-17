import pygame
import math
from core.config_load import config

# Load configurations
constants = config.load_constants()['physics']
colors = config.load_colors()
display_settings = config.load_display_settings()

# Constants
WINDOW_WIDTH = display_settings['window']['width']
WINDOW_HEIGHT = display_settings['window']['height']
WHITE = tuple(colors['white'])
YELLOW = tuple(colors['yellow'])
AU = constants['AU']
SCALE = 200/AU

class Renderer:
    """Handles all drawing operations for the simulation"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.large_font = pygame.font.SysFont(display_settings['font']['name'], 
                                            display_settings['font']['size'] + 4)
        self.frame_count = 0
    
    def draw_body(self, body):
        """Draw a celestial body with its orbit trail and information"""
        self.frame_count += 1
        
        screen_x = body.x*SCALE + WINDOW_WIDTH/2
        screen_y = body.y*SCALE + WINDOW_HEIGHT/2    

        # Debug: Print screen coordinates every 60 frames
        if self.frame_count % 60 == 0:
            print(f"Drawing body at screen coords: ({screen_x:.1f}, {screen_y:.1f}), world coords: ({body.x:.1f}, {body.y:.1f})")

        # Check if body is visible on screen
        if (screen_x < -100 or screen_x > WINDOW_WIDTH + 100 or 
            screen_y < -100 or screen_y > WINDOW_HEIGHT + 100):
            # Draw a small indicator for off-screen bodies
            if screen_x < 0:
                screen_x = 20
            elif screen_x > WINDOW_WIDTH:
                screen_x = WINDOW_WIDTH - 20
            if screen_y < 0:
                screen_y = 20
            elif screen_y > WINDOW_HEIGHT:
                screen_y = WINDOW_HEIGHT - 20
            
            # Draw small indicator
            pygame.draw.circle(self.screen, body.color, (int(screen_x), int(screen_y)), 5)
            indicator_text = self.font.render("OFF-SCREEN", 1, WHITE)
            self.screen.blit(indicator_text, (screen_x + 10, screen_y))
            return

        # Draw orbit trail
        if len(body.orbit) > 2:
            updated_points = []
            for point in body.orbit:
                orbit_x, orbit_y = point
                orbit_x += WINDOW_WIDTH/2
                orbit_y += WINDOW_HEIGHT/2
                # Only add points that are on screen
                if 0 <= orbit_x <= WINDOW_WIDTH and 0 <= orbit_y <= WINDOW_HEIGHT:
                    updated_points.append((orbit_x, orbit_y))
        
            if len(updated_points) > 1:
                pygame.draw.lines(self.screen, body.color, False, updated_points, 2)

        # Draw the body
        pygame.draw.circle(self.screen, body.color, (int(screen_x), int(screen_y)), body.radius)

        # Draw basic information
        self._draw_body_info(body, screen_x, screen_y)
    
    def _draw_body_info(self, body, x, y):
        """Draw velocity and position information"""
        speed = body.get_speed()
        info_texts = [
            f"Vx={round(body.x_vel,2)}m/s",
            f"Vy={round(body.y_vel,2)}m/s", 
            f"Pos=({round(body.x*SCALE,1)}, {round(body.y*SCALE,1)})"
        ]
        
        for i, text in enumerate(info_texts):
            rendered_text = self.font.render(text, 1, WHITE)
            self.screen.blit(rendered_text, (x + 20, y + i * 18))
    
    def draw_simulation_info(self, time_manager, collision_count):
        """Draw basic simulation information"""
        y_offset = 10
        
        # Simulation time
        time_text = f"Time: {time_manager.get_formatted_time()}"
        time_surface = self.large_font.render(time_text, 1, YELLOW)
        self.screen.blit(time_surface, (10, y_offset))
        y_offset += 30
        
        # Time step info
        timestep_hours = time_manager.time_step_per_frame / 3600
        timestep_text = f"Time step: {timestep_hours:.1f} hours per frame"
        timestep_surface = self.font.render(timestep_text, 1, WHITE)
        self.screen.blit(timestep_surface, (10, y_offset))
        y_offset += 20
        
        # FPS
        fps_text = f"FPS: {time_manager.fps}"
        fps_surface = self.font.render(fps_text, 1, WHITE)
        self.screen.blit(fps_surface, (10, y_offset))
        y_offset += 20
        
        # Collision count
        collision_text = f"Collisions: {collision_count}"
        collision_surface = self.font.render(collision_text, 1, WHITE)
        self.screen.blit(collision_surface, (10, y_offset))
        y_offset += 20
        
        # Screen center indicator
        center_text = f"Screen center: ({WINDOW_WIDTH//2}, {WINDOW_HEIGHT//2})"
        center_surface = self.font.render(center_text, 1, WHITE)
        self.screen.blit(center_surface, (10, y_offset))
        