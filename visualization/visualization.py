import sys
import pygame
import numpy as np

# Configuration
WIDTH, HEIGHT = 800, 800
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)  # White
PARTICLE_COLOR = (0, 0, 255)        # Blue
CONTAINER_COLOR = (0, 0, 0)         # Black
OBSTACLE_COLOR = (255, 0, 0)        # Red

# Physics scaling
CONTAINER_RADIUS = 0.05
SCALE_FACTOR = min(WIDTH, HEIGHT) / (2 * CONTAINER_RADIUS * 1.1)  # Add 10% padding

def parse_simulation_file(filename):
    """Parse the simulation output file"""
    frames = []
    with open(filename, "r") as f:
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
            radius = float(parts[4])
            particles.append((x, y, radius))
            idx += 1

        frames.append((time, np.array(particles)))

    return frames

def pygame_coords(x, y):
    """Convert simulation coordinates to pygame screen coordinates"""
    screen_x = WIDTH // 2 + x * SCALE_FACTOR
    screen_y = HEIGHT // 2 - y * SCALE_FACTOR  # Flip y-axis
    return int(screen_x), int(screen_y)

def pygame_radius(radius):
    """Convert simulation radius to pygame pixels"""
    return max(1, int(radius * SCALE_FACTOR))  # Ensure at least 1 pixel

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 18)

    frames = parse_simulation_file(sys.argv[1])
    current_frame = 0
    paused = False
    show_help = True

    # Precompute all positions in screen coordinates
    screen_positions = []
    for time, particles in frames:
        frame_data = []
        for x, y, r in particles:
            screen_x, screen_y = pygame_coords(x, y)
            screen_r = pygame_radius(r)
            frame_data.append((screen_x, screen_y, screen_r))
        screen_positions.append(frame_data)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_h:
                    show_help = not show_help
                elif event.key == pygame.K_RIGHT and paused:
                    current_frame = min(current_frame + 1, len(frames) - 1)
                elif event.key == pygame.K_LEFT and paused:
                    current_frame = max(current_frame - 1, 0)

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # Draw container
        pygame.draw.circle(
            screen, CONTAINER_COLOR,
            (WIDTH // 2, HEIGHT // 2),
            int(CONTAINER_RADIUS * SCALE_FACTOR),
            1  # Line width
        )

        # Draw particles
        for x, y, r in screen_positions[current_frame]:

            pygame.draw.circle(screen, PARTICLE_COLOR, (x, y), r)

        # Draw obstacle (if present)
        obstacle_radius = pygame_radius(0.005)
        pygame.draw.circle(
            screen, OBSTACLE_COLOR,
            (WIDTH // 2, HEIGHT // 2),
            obstacle_radius,
            1  # Line width
        )

        # Display time
        time_text = font.render(f"Time: {frames[current_frame][0]:.3e}", True, (0, 0, 0))
        screen.blit(time_text, (10, 10))

        # Display help
        if show_help:
            help_text = [
                "SPACE: Pause/Play",
                "LEFT/RIGHT: Step frames (when paused)",
                "H: Toggle help"
            ]
            for i, text in enumerate(help_text):
                rendered = font.render(text, True, (0, 0, 0))
                screen.blit(rendered, (10, 40 + i * 20))

        pygame.display.flip()

        if not paused:
            current_frame = (current_frame + 1) % len(frames)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pygame_animation.py <simulation_file>")
        sys.exit(1)
    main()