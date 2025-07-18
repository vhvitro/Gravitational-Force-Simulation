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

## Project Structure

```
Gravitational-Force-Simulation/
├── config/                 # Configuration files
│   ├── constants.json     # Physics constants and simulation settings
│   ├── colors.json       # Color definitions
│   └── display.json      # Display settings
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

## Creating Bodies

Bodies are defined in `main.py` with these parameters:
```python
Body(x, y, color, mass, radius, x_vel, y_vel)
```

Example setup:
```python
bodies = [
    Body(0, 0, YELLOW, 1*SUN_MASS, 10, 0, 0),                    # Central star
    Body(400/SCALE, 0, LIME_GREEN, 0.000001*SUN_MASS, 5, 0, 15000)  # Orbiting body
]
```

Positions and velocities use real units (meters, m/s), with automatic scaling for display.

## Configuration

### Physics Constants (`config/constants.json`)
```json
{
    "physics": {
        "gravitational_constant": 6.67428e-11,
        "absorption_coefficient": 0.8,
        "collision_threshold": 1000,
        "mass_ratio_threshold": 1000,
        "black_hole_mass": 1e10
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
- Coordinate system: real meters, converted to pixels for display
- Collision detection based on radius overlap
- History system stores 5000 states for rewind functionality
- Optimized for 60 FPS with moderate number of bodies

## Limitations

This simulation uses Newtonian mechanics and simplified models. It's designed for educational purposes and visual demonstration, not as a rigorous astronomical simulation tool.

---

*A physics simulation balancing educational value with computational simplicity.*