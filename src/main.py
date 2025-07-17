import pygame
from core.config_load import config
from core.objects import Body, delete_body
from core.physics import handle_collision, new_bodies_queue
from graphics.renderer import Renderer

def main():
    """Main simulation loop"""
    # Initialize Pygame
    pygame.init()
    
    # Load configurations
    colors = config.load_colors()
    display_settings = config.load_display_settings()
    
    # Setup display
    WINDOW_WIDTH = display_settings['window']['width']
    WINDOW_HEIGHT = display_settings['window']['height']
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(display_settings['window']['title'])
    
    # Setup font and renderer
    font = pygame.font.SysFont(display_settings['font']['name'], display_settings['font']['size'])
    renderer = Renderer(screen, font)
    
    # Colors
    DARK_BLUE = tuple(colors['dark_blue'])
    YELLOW = tuple(colors['yellow'])
    LIME_GREEN = tuple(colors['lime_green'])
    ORANGE = tuple(colors['orange'])
    CYAN = tuple(colors['cyan'])
    MERCURY_RED = tuple(colors['mercury_red'])
    
    # Initialize simulation
    clock = pygame.time.Clock()
    collision_count = 0
    
    # Create initial celestial bodies (from original gravity_open.py)
    bodies = [
        Body(0, 0, YELLOW, 10**14, 30, 0, 0),
        Body(-600, -200, LIME_GREEN, 10**13, 20, -2, 1),
        Body(-500, 200, ORANGE, 10**9, 10, -2, 1),
        Body(650, -300, CYAN, 10**9, 10, -2, 3),
        Body(-400, -30, MERCURY_RED, 10**9, 10, 0.3, 0.5)
    ]
    
    # Calculate total system mass
    total_mass = sum(body.mass for body in bodies)
    print(f'System has total mass of {total_mass}')
    
    # Main simulation loop
    running = True
    while running:
        clock.tick(60)
        screen.fill(DARK_BLUE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Add new bodies from physics interactions
        if len(new_bodies_queue) >= 1:
            bodies.extend(new_bodies_queue)
            new_bodies_queue.clear()

        # Update and draw bodies
        for body in bodies[:]:  # Use slice to avoid modification during iteration
            if not body.exists:
                delete_body(body, bodies)
            else:
                body.update_position(bodies)
                renderer.draw_celestial_body(body)
                
                # Check collisions with other bodies
                for other_body in bodies:
                    if other_body == body:
                        continue
                    if handle_collision(body, other_body):
                        collision_count += 1

        # Draw UI elements
        renderer.draw_collision_counter(collision_count)
        
        pygame.display.update()

    # Cleanup
    pygame.quit()
    
    # Print final masses
    for i, body in enumerate(bodies, 1):
        print(f'Body {i} has mass of {body.mass}')

if __name__ == "__main__":
    main()