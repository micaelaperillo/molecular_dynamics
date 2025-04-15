import pygame
import sys
import time

particles = [[(-0.04842, -0.007698),
  (-0.01971, -0.008743),
  (0.013665, 0.036878),
  (-0.009355, -0.001953),
  (0.009562, -0.023822),
  (0.018944, 0.015233),
  (0.03159, 0.006699),
  (-0.031648, 0.030938),
  (0.034822, 0.012496),
  (0.023582, -0.010181),
  (-0.013573, 0.015853),
  (0.011387, -0.037805),
  (-0.01318, -0.014928),
  (-0.011007, -0.000752),
  (0.040793, -0.010266),
  (0.033038, -0.013617),
  (-0.030098, -0.032369),
  (0.015668, 0.045278),
  (-0.018835, 0.017498),
  (0.008506, -0.038522),
  (0.041963, 0.019117),
  (-0.038599, 0.021106),
  (0.011179, -0.010365),
  (-0.047001, 0.014549),
  (-0.021539, 0.001834),
  (-0.030749, 0.03397),
  (0.038438, 0.009558),
  (0.03364, 0.01856),
  (0.033734, 0.00044),
  (0.035727, -0.028739)],
 [(-0.049214, -0.00686),
  (-0.019655, -0.008984),
  (0.01271, 0.036285),
  (-0.009106, -0.001608),
  (0.00986, -0.023517),
  (0.019437, 0.015374),
  (0.031922, 0.006703),
  (-0.031145, 0.03006),
  (0.035656, 0.013427),
  (0.024542, -0.009601),
  (-0.01403, 0.01531),
  (0.011709, -0.03747),
  (-0.012882, -0.014797),
  (-0.010979, 0.000169),
  (0.040583, -0.010896),
  (0.033921, -0.014555),
  (-0.029589, -0.03206),
  (0.016332, 0.046023),
  (-0.019685, 0.017602),
  (0.008114, -0.03913),
  (0.041036, 0.018461),
  (-0.038381, 0.020339),
  (0.01123, -0.009445),
  (-0.047313, 0.013792),
  (-0.020553, 0.00137),
  (-0.030299, 0.034352),
  (0.038288, 0.010517),
  (0.034038, 0.01902),
  (0.03332, 6.8e-05),
  (0.036073, -0.028511)],
 [(-0.049815, -0.006755),
  (-0.019148, -0.008976),
  (0.012547, 0.035859),
  (-0.009593, -0.00205),
  (0.009595, -0.023711),
  (0.019873, 0.015075),
  (0.031082, 0.007051),
  (-0.030694, 0.029346),
  (0.03558, 0.014218),
  (0.023729, -0.009604),
  (-0.013398, 0.015497),
  (0.010962, -0.037029),
  (-0.012055, -0.014332),
  (-0.010572, 0.000772),
  (0.039964, -0.011287),
  (0.03483, -0.014871),
  (-0.02964, -0.031605),
  (0.016756, 0.045549),
  (-0.01939, 0.016978),
  (0.008148, -0.039513),
  (0.041571, 0.017992),
  (-0.039121, 0.020758),
  (0.011588, -0.010265),
  (-0.048257, 0.012856),
  (-0.01986, 0.000489),
  (-0.029825, 0.033996),
  (0.038919, 0.010295),
  (0.03452, 0.019063),
  (0.03276, -0.0003),
  (0.036323, -0.028928)]]

obstacle_r = 0.005
L = 0.1
particle_r = 0.0005
multiplier = 2.5

data_obs_moving = {
    'L': L,
    'particle_r': particle_r,
    'steps': {
        0: particles[0],
        1: particles[1],
        2: particles[2]
    },
    'obstacle': {
        'obstacle_r': obstacle_r,
        'is_moving': True,
        'steps': {
            0: (0, 0),
            1: (0.005, 0),
            2: (0.01, 0)
        }

    }
}

data_obs_not_moving = {
    'L': L,
    'particle_r': particle_r,
    'steps': {
        0: particles[0],
        1: particles[1],
        2: particles[2]
    },
    'obstacle': {
        'obstacle_r': obstacle_r,
        'is_moving': False

    }
}

colors = {
    'background': '#E0E0E0', 
    'border': "#212121",  
    'obstacle': '#616161',
    'particle': "#212121" 
}

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Simulacion de Sistemas - TP3")

    center = (width // 2, height // 2)

    data = data_obs_not_moving

    L_scaled = data['L'] * multiplier
    obstacle_r_scaled = data['obstacle']['obstacle_r'] * multiplier
    particle_r_scaled = data['particle_r'] * multiplier

    steps = list(data['steps'].values())
    step_index = 0
    pause = True

    while True:
        screen.fill(colors['background'])

        pygame.draw.circle(screen, colors['border'], center, int(L_scaled * width), width=5) # Circulo exterior

        current_particles = steps[step_index]
        for x, y in current_particles:
            px = int(center[0] + (x / L) * (L_scaled * width / 2))
            py = int(center[1] + (y / L) * (L_scaled * height / 2))
            pygame.draw.circle(screen, colors['particle'], (px, py), int(particle_r_scaled * width))

        if data['obstacle']['is_moving']:
            x, y = data['obstacle']['steps'][step_index]
            px = int(center[0] + (x / L) * (L_scaled * width / 2))
            py = int(center[1] + (y / L) * (L_scaled * height / 2))
            pygame.draw.circle(screen, colors['obstacle'], (px, py), int(obstacle_r_scaled * width), width=0)
        else:
            pygame.draw.circle(screen, colors['obstacle'], center, int(obstacle_r_scaled * width), width=0)

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
