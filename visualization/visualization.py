import pygame
import sys
import time

particles = [
    [(0.1, 0.2), (0.2, 0.3), (0.3, 0.4)],
    [(0.15, 0.25), (0.25, 0.35), (0.35, 0.45)],
    [(0.2, 0.3), (0.3, 0.4), (0.4, 0.5)]
]

obstacle_r = 0.05
L = 0.1
particle_r = 0.005
multiplier = 2.75

data = {
    'obstacle_r': obstacle_r,
    'L': L,
    'particle_r': particle_r,
    'steps': {
        '0': particles[0],
        '1': particles[1],
        '2': particles[2]
    }
}

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Simulacion de Sistemas - TP3")

    center = (width // 2, height // 2)
    bg_color = (255, 255, 255)
    circle_color = (0, 0, 0)
    particle_color = (160, 160, 160)

    L_scaled = data['L'] * multiplier
    obstacle_r_scaled = data['obstacle_r'] * multiplier
    particle_r_scaled = data['particle_r'] * multiplier

    steps = list(data['steps'].values())
    step_index = 0
    pause = True

    while True:
        screen.fill(bg_color)

        pygame.draw.circle(screen, circle_color, center, int(L_scaled * width), width=3) # Circulo exterior
        pygame.draw.circle(screen, circle_color, center, int(obstacle_r_scaled * width), width=0) # Obstaculo

        # Particulas
        current_particles = steps[step_index]
        for x, y in current_particles:
            px = int(center[0] + (x - 0.5) * width)
            py = int(center[1] + (y - 0.5) * height)
            pygame.draw.circle(screen, particle_color, (px, py), int(particle_r_scaled * width))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()

        if not pause:
            step_index = (step_index + 1) % len(steps)
            time.sleep(0.5) 


if __name__ == "__main__":
    main()
