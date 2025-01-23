from vpython import *
import numpy as np

# Physical parameters
sphere_radius = 0.1  # meters
sphere_mass = 1.0    # kg
initial_height = 2.0 # meters
gravity = vector(0, -9.81, 0)  # m/s^2
coefficient_of_restitution = 1.0

# Initial angular and linear velocities
initial_velocity = vector(1, 0, 0)  # horizontal velocity
initial_omega = vector(10, 20, 30)

# Create scene
scene = canvas(title='Sphere Realistic Bounce', width=800, height=600, 
               center=vector(0,1,0), background=color.white)

# Create sphere
sphere = sphere(pos=vector(0, initial_height, 0), 
                radius=sphere_radius, 
                color=color.blue, 
                make_trail=True)

# Ground
ground = box(pos=vector(0, 0, 0), 
             size=vector(2, 0.1, 2), 
             color=color.green)

# Physics parameters
dt = 0.01  # time step
t = 0
collision_count = 0

# Initial conditions
sphere.velocity = initial_velocity + vector(0, 0, 0)
sphere.velocity.y = 0
sphere.omega = initial_omega

# Collision details tracking
collision_details = []

# Simulation
while collision_count < 3:
    rate(100)  # Limit computation speed
    
    # Update position
    sphere.pos += sphere.velocity * dt
    
    # Update velocity (gravity)
    sphere.velocity += gravity * dt
    
    # Collision detection with ground
    if sphere.pos.y <= sphere_radius:
        # Record collision details
        collision_details.append({
            'time': t,
            'velocity_before': sphere.velocity,
            'position': sphere.pos
        })
        
        # Apply coefficient of restitution to both horizontal and vertical velocities
        sphere.velocity.y = -sphere.velocity.y * coefficient_of_restitution
        
        # Maintain horizontal velocity
        sphere.velocity.x *= coefficient_of_restitution
        sphere.velocity.z *= coefficient_of_restitution
        
        # Reposition sphere to ground surface
        sphere.pos.y = sphere_radius
        
        collision_count += 1
    
    # Rotation dynamics
    rotation_axis = norm(sphere.omega)
    sphere.rotate(angle=mag(sphere.omega) * dt, 
                  axis=rotation_axis)
    
    t += dt

# Print collision details
print("Collision Details:")
for i, collision in enumerate(collision_details, 1):
    print(f"Collision {i}:")
    print(f"  Time: {collision['time']:.2f} s")
    print(f"  Velocity Before: {collision['velocity_before']}")
    print(f"  Position: {collision['position']}")