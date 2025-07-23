# Gravitational-Force-Simulation

A gravitational force simulation applying Newton's Universal Law of Gravitation in Python using pygame. This project applies the equation **F = G·m₁·m₂/d²** with additional simple models for body interactions.

## What it does

The core physics uses real gravitational force calculations and proper conservation of momentum. I've also implemented some simple models for:
- **Absorption mechanics** - mass-based interaction when bodies collide
- **Black hole formation** - massive objects can merge based on mass thresholds
- **Debris creation** - simple ejection model during certain collisions
- **Orbit trails** - visual tracking of body trajectories

*Note: The absorption, black hole, and debris features are simplified models - not rigorous physics simulations.*

## Features

- **Pause/Resume**: Hit `SPACE` to pause the simulation
- **Rewind**: Hold `LEFT ARROW` while paused to step back through history (up to 5000 states)
- **Real physics**: Uses actual gravitational constant and astronomical units
- **Scaling system**: Converts between real astronomical distances and screen pixels
- **Real-time info**: Displays velocities, positions, and other data for each body
- **JSON configuration**: Easy setup of initial bodies without editing code

## Project Structure

```
Gravitational-Force-Simulation/
├── config/                 # Configuration files
│   ├── constants.json     # Physics constants and simulation settings
│   ├── colors.json       # Color definitions
│   ├── display.json      # Display settings
│   └── bodies.json       # Initial bodies configuration
├── src/                   # Source code
│   ├── main.py           # Main simulation loop
│   ├── core/             # Physics and object classes
│   └── graphics/         # Rendering system
└── README.md            # This file
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/vhvitro/Gravitational-Force-Simulation.git
cd Gravitational-Force-Simulation
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the simulation:
```bash
cd src
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Pause/Resume simulation |
| `LEFT ARROW` | Rewind (while paused) |
| `ESC` | Exit |

## Configuring Initial Bodies

Each body in the JSON file has the following structure:

```json
{
    "name": "Body Name",
    "position": {
        "x_au": 0,          // Position in pixels (screen coordinates)
        "y_au": 0           // OR use "x" and "y" for meters (real coordinates)
    },
    "color": "color_name",  // Color from colors.json
    "mass_multiplier": 1.0, // Multiplier for mass unit
    "mass_unit": "sun_mass", // "sun_mass" or "kg"
    "radius": 10,           // Visual radius in pixels
    "velocity": {
        "x": 0,             // Velocity in m/s
        "y": 0
    }
}
```

### Position Options

You can specify position in two ways:

**Option 1 - Screen coordinates (pixels):**
```json
"position": {
    "x_au": 200,    // 200 pixels from center
    "y_au": 100     // 100 pixels from center
}
```

**Option 2 - Real coordinates (meters):**
```json
"position": {
    "x": 1.496e11,  // 1 AU in meters
    "y": 0
}
```

### Example Configurations

**Simple Earth-Sun System:**
```json
{
    "initial_bodies": [
        {
            "name": "Sun",
            "position": {"x": 0, "y": 0},
            "color": "yellow",
            "mass_multiplier": 1.0,
            "mass_unit": "sun_mass",
            "radius": 30,
            "velocity": {"x": 0, "y": 0}
        },
        {
            "name": "Earth",
            "position": {"x_au": 200, "y_au": 0},
            "color": "cyan",
            "mass_multiplier": 3e-6,
            "mass_unit": "sun_mass",
            "radius": 8,
            "velocity": {"x": 0, "y": 29780}
        }
    ]
}
```

### Available Colors

Colors must match those defined in `config/colors.json`:
- `yellow`, `orange`, `mercury_red`
- `lime_green`, `cyan`, `neptune_blue`
- `bronze`, `white`, `black`, `dark_blue`

### Mass Units

- **`sun_mass`**: Use solar masses (1.989e30 kg)
  - Example: `"mass_multiplier": 0.5` = 0.5 solar masses
- **`kg`**: Use kilograms directly
  - Example: `"mass_multiplier": 5.972e24` = Earth mass

### Creating Your Own Scenarios

1. Edit `config/bodies.json`
2. Add/remove/modify bodies in the `initial_bodies` array
3. Save the file and run the simulation
4. No code changes required!

**Tips for stable orbits:**
- For circular orbits around a central mass: `v = √(GM/r)`
- Start with positions on axes (x or y = 0) for simplicity
- Use tangential velocities (perpendicular to position vector)

## Configuration

### Physics Constants (`config/constants.json`)
```json
{
    "physics": {
        "gravitational_constant": 6.67428e-11,
        "absorption_coefficient": 0.8,
        "collision_threshold": 1000,
        "mass_ratio_threshold": 1000,
        "black_hole_mass": 1e10,
        "sun_mass": 1.989e30,
        "AU": 1.496e11
    },
    "simulation": {
        "time_step_per_frame": 86400,
        "target_fps": 60
    }
}
```

- **absorption_coefficient**: Controls mass retention vs. ejection (0-1)
- **time_step_per_frame**: Simulation time per frame (default: 1 day)
- **mass_ratio_threshold**: Threshold for absorption vs. collision behavior

## Simple Models vs. Rigorous Physics

**Rigorous physics:**
- Gravitational force calculations (F = Gm₁m₂/r²)
- Conservation of momentum in collisions
- Orbital mechanics with real constants

**Simple models:**
- Mass-based absorption during collisions
- Threshold-based black hole formation
- Simplified debris ejection mechanics
- Close-encounter handling

These simple models provide interesting interactions while keeping the simulation approachable and computationally efficient.

## Technical Notes

- Uses fixed time steps for stability
- Coordinate system: real meters for physics, pixels for display
- Collision detection based on radius overlap
- History system stores 5000 states for rewind functionality
- Optimized for 60 FPS with moderate number of bodies
- Scale factor: 200 pixels ≈ 1 AU

## Limitations

This simulation uses Newtonian mechanics and simplified models. It's designed for educational purposes and visual demonstration, not as a rigorous astronomical simulation tool.

---

*A physics simulation balancing educational value with computational simplicity.*