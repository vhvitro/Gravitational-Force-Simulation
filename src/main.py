import pygame
from core.config_load import config
from core.objects import Body, delete_body
from core.physics import handle_collision, new_bodies_queue
from core.time_manager import TimeManager
from graphics.renderer import Renderer

def main():
    """Main simulation loop with fixed time step"""
    # Initialize Pygame
    pygame.init()
    
    # Load configurations
    colors = config.load_colors()
    display_settings = config.load_display_settings()
    simulation_config = config.load_constants()['simulation']
    constants = config.load_constants()['physics']

    #Constants
    AU = constants['AU']
    SCALE = 200/AU
    SUN_MASS = constants['sun_mass']
    
    # Setup display
    WINDOW_WIDTH = display_settings['window']['width']
    WINDOW_HEIGHT = display_settings['window']['height']
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(display_settings['window']['title'])
    
    # Setup font and renderer
    font = pygame.font.SysFont(display_settings['font']['name'], display_settings['font']['size'])
    renderer = Renderer(screen, font)
    
    # Initialize time manager
    time_manager = TimeManager()
    
    # Colors
    DARK_BLUE = tuple(colors['dark_blue'])
    YELLOW = tuple(colors['yellow'])
    LIME_GREEN = tuple(colors['lime_green'])
    ORANGE = tuple(colors['orange'])
    CYAN = tuple(colors['cyan'])
    MERCURY_RED = tuple(colors['mercury_red'])
    
    # Initialize simulation
    target_fps = simulation_config['target_fps']
    clock = pygame.time.Clock()
    collision_count = 0
    
    # Create initial celestial bodies (same as original but with time step)
    bodies = [
        Body(0, 0, YELLOW, 1*SUN_MASS, 10, 0, 0),
        Body(-600/SCALE, -200/SCALE, LIME_GREEN, 1e-6*SUN_MASS, 5, 0, 10000),
        Body(-400/SCALE, -30/SCALE, MERCURY_RED, 1E-3*SUN_MASS, 8, 3000, 7000)
    ]
    
    # Calculate total system mass
    total_mass = sum(body.mass for body in bodies)
    print(f'System has total mass of {total_mass}')
    print(f'Time step: {time_manager.time_step_per_frame/3600:.1f} hours per frame')
    print(f'Target FPS: {target_fps}')
    
    # Main simulation loop
    running = True
    while running:
        clock.tick(target_fps)  # Fixed FPS
        screen.fill(DARK_BLUE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update time (one step per frame)
        time_manager.update()
        
        # Get the fixed time step
        dt = time_manager.get_time_step()

        # Add new bodies from physics interactions
        if len(new_bodies_queue) >= 1:
            bodies.extend(new_bodies_queue)
            new_bodies_queue.clear()

        # Update and draw bodies
        for body in bodies[:]:  # Use slice to avoid modification during iteration
            if not body.exists:
                delete_body(body, bodies)
            else:
                body.update_position(bodies, dt)
                renderer.draw_body(body)
                
                # Check collisions with other bodies
                for other_body in bodies:
                    if other_body == body:
                        continue
                    if handle_collision(body, other_body):
                        collision_count += 1

        # Draw simulation info
        renderer.draw_simulation_info(time_manager, collision_count)
        
        pygame.display.update()

    # Cleanup
    pygame.quit()
    
    # Print final masses
    print(f'\nSimulation ended after {time_manager.get_formatted_time()}')
    for i, body in enumerate(bodies, 1):
        if body.exists:
            print(f'Body {i} has mass of {body.mass}')

if __name__ == "__main__":
    main()