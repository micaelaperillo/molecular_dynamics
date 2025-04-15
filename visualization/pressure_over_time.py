import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def parse_simulation_file(file_path):
    pressure_data = []
    particle_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        n = int(lines[i].strip())
        i += 1

        while i < len(lines):
            t = float(lines[i].strip())
            i += 1
            wallPressure = float(lines[i].strip())
            i += 1
            obstaclePressure = float(lines[i].strip())
            i += 1
            pressure_data.append([t, wallPressure, obstaclePressure])
            for _ in range(n):
                x, y, vx, vy = map(float, lines[i].strip().split())
                particle_data.append([t, x, y, vx, vy])
                i += 1

    df_pressure = pd.DataFrame(pressure_data, columns=['time', 'wallPressure', 'obstaclePressure'])
    df_particles = pd.DataFrame(particle_data, columns=['time', 'x', 'y', 'vx', 'vy'])
    return df_pressure, df_particles


def plot_pressure_over_time(df_pressure):
    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['wallPressure'], label='Presión Paredes', color='blue')
    plt.plot(df_pressure['time'], df_pressure['obstaclePressure'], label='Presión Obstaculo', color='red')
    plt.plot(df_pressure['time'], df_pressure['wallPressure'] + df_pressure['obstaclePressure'],
             label='Presión Total', color='green', linestyle='--')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Presión [N/m]')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    directory = sys.argv[1]
    df_pressure, df_particles = parse_simulation_file(directory)
    print(df_pressure)
    print(df_particles)
    plot_pressure_over_time(df_pressure)


if __name__ == "__main__":
    main();

