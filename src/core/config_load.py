import json
import os
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        # Get the project root directory (2 levels up from this file)
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
    
    def load_constants(self):
        """Load physics constants from JSON file"""
        config_path = self.config_dir / "constants.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
            return data['physics']
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
    
    def load_colors(self):
        """Load color definitions from JSON file"""
        config_path = self.config_dir / "colors.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
    
    def load_display_settings(self):
        """Load display settings from JSON file"""
        config_path = self.config_dir / "display.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
    def load_bodies(self):
        """Load initial bodies configuration from JSON file"""
        config_path = self.config_dir / "bodies.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
        
# Create a global instance for easy access
config = ConfigLoader()