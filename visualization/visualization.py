import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np


CONTAINER_RADIUS = 0.05
OBSTACLE_RADIUS = 0.005
PARTICLE_RADIUS = 0.0005

obstacle_present=True

def parse_simulation_file():
    frames = []
    with open(sys.argv[1], "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    N = int(lines[idx])
    idx += 1

    while idx < len(lines):

        time = float(lines[idx])
        wall_pressure = float(lines[idx + 1])
        obstacle_pressure = float(lines[idx + 2])
        idx += 3

        particles = []
        for _ in range(N):
            parts = lines[idx].split()
            x, y = float(parts[0]), float(parts[1])
            radius=float(parts[4])
            if radius==OBSTACLE_RADIUS:
                obstacle_present=True
            particles.append((x, y,radius))
            idx += 1

        frames.append((time, np.array(particles)))


    return frames

frames = parse_simulation_file()

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-CONTAINER_RADIUS, CONTAINER_RADIUS)
ax.set_ylim(-CONTAINER_RADIUS, CONTAINER_RADIUS)

# Draw static background: container and obstacle
container = Circle((0, 0), CONTAINER_RADIUS, color='black', fill=False, lw=2)
ax.add_patch(container)
if obstacle_present:
    obstacle = Circle((0, 0), OBSTACLE_RADIUS, color='red', fill=False, lw=2)
    ax.add_patch(obstacle)



# --- after you create the patches ---
initial_positions = frames[0][1]
particle_patches = [
    Circle((x, y), r, color='blue') for (x, y,r) in initial_positions
]
for patch in particle_patches:
    ax.add_patch(patch)

time_text = ax.text(-0.48, 0.46, '', fontsize=10, color='gray')

def animate(i):
    time, particles = frames[i]
    for patch, (x, y,r) in zip(particle_patches, particles):
        patch.center = (x, y)
    time_text.set_text(f"t = {time:.3e}")
    return particle_patches + [time_text]

ani = animation.FuncAnimation(fig, animate, frames=len(frames), interval=15, blit=False)
plt.title("Particle Simulation with Obstacle")
plt.show()
