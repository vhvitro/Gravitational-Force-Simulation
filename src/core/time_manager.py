import time
from core.config_load import config

class TimeManager:
    """Simple time manager with fixed time step"""
    
    def __init__(self):
        self.config = config.load_constants()['simulation']
        
        # Fixed time step per frame (in seconds)
        self.time_step_per_frame = self.config['time_step_per_frame']
        
        # Simulation time tracking
        self.simulation_time = 0.0  # Total simulation time in seconds
        self.frame_count = 0
        
        # FPS tracking
        self.fps = 0
        self.last_fps_update = time.time()
        self.fps_frame_count = 0
    
    def update(self):
        """Update simulation time by one time step"""
        self.simulation_time += self.time_step_per_frame
        self.frame_count += 1
        
        # Update FPS counter every second
        self.fps_frame_count += 1
        current_time = time.time()
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.fps_frame_count
            self.fps_frame_count = 0
            self.last_fps_update = current_time
    
    def get_time_step(self):
        """Get the fixed time step"""
        return self.time_step_per_frame
    
    def get_formatted_time(self):
        """Get formatted simulation time string"""
        days = self.simulation_time / 86400
        if days < 1:
            hours = self.simulation_time / 3600
            return f"{hours:.1f} hours"
        elif days < 365:
            return f"{days:.1f} days"
        else:
            years = days / 365.25
            return f"{years:.2f} years"
    
    def reset_time(self):
        """Reset simulation time"""
        self.simulation_time = 0.0
        self.frame_count = 0

    def rewind(self):
        self.simulation_time -= self.time_step_per_frame
        self.frame_count -=1
        