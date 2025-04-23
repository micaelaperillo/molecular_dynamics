import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def parse_simulation_file(file_path):
    pressure_data = []
    particle_data = []
    collision_data = []
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
            temperature = float(lines[i].strip())
            i += 1
            firstTimeCollisions = int(lines[i].strip())
            i += 1
            totalCollisions = int(lines[i].strip())
            i += 1
            pressure_data.append([t, wallPressure, obstaclePressure, temperature])
            collision_data.append([t, firstTimeCollisions, totalCollisions])
            for _ in range(n):
                x, y, vx, vy, r = map(float, lines[i].strip().split())
                particle_data.append([t, x, y, vx, vy, r])
                i += 1

    df_pressure = pd.DataFrame(pressure_data, columns=['time', 'wallPressure', 'obstaclePressure', 'temperature'])
    df_obstacle_collisions = pd.DataFrame(collision_data, columns=['time', 'firstTimeCollisions', 'totalCollisions'])
    df_particles = pd.DataFrame(particle_data, columns=['time', 'x', 'y', 'vx', 'vy', 'radius'])
    return df_pressure, df_obstacle_collisions, df_particles


def plot_collisions_over_time(df_collisions):
    plt.figure(figsize=(10, 6))
    plt.plot(df_collisions['time'], df_collisions['firstTimeCollisions'], label='Colisiones primerizas', color='blue')
    plt.plot(df_collisions['time'], df_collisions['totalCollisions'], label='Total de colisiones', color='red')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Cantidad de Colisiones')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/collisions_over_time.png')
    plt.show()


def calculate_collision_rate(df_collisions, df_pressure):
    total_time = df_collisions['time'].iloc[-1]
    total_collisions = df_collisions['totalCollisions'].iloc[-1]
    collision_rate = total_collisions / total_time
    temperature = df_pressure['temperature'].mean()
    print(f"Taza de colisión: {collision_rate:.2f} collision/s a Temperatura: {temperature:.2f} K")


def plot_pressure_over_time(df_pressure, use_log_scale=False):
    total_pressure = df_pressure['wallPressure'] + df_pressure['obstaclePressure']

    # Equilibrium value: average of the last 10% of total pressure
    equilibrium_pressure = total_pressure.iloc[int(0.9 * len(total_pressure)):].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['wallPressure'], label='Presión Pared', color='blue')
    plt.plot(df_pressure['time'], df_pressure['obstaclePressure'], label='Presión Obstaculo', color='red')
    plt.plot(df_pressure['time'], total_pressure, label='Presión Total', color='green', linestyle='--')

    # Draw equilibrium line
    plt.axhline(equilibrium_pressure, color='gray', linestyle=':', label=f'Equilibrio ≈ {equilibrium_pressure:.0f} N/m')

    plt.xlabel('Tiempo [s]')
    plt.ylabel('Presión [N/m]')
    if use_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/pressure_over_time.png')
    plt.show()


def plot_individual_pressures(df_pressure, use_log_scale=False):
    total_pressure = df_pressure['wallPressure'] + df_pressure['obstaclePressure']

    # Plot wall pressure
    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['wallPressure'], label='Presión Pared', color='blue')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Presión [N/m]')
    if use_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/wall_pressure.png')
    plt.close()

    # Plot obstacle pressure
    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['obstaclePressure'], label='Presión Obstaculo', color='red')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Presión [N/m]')
    if use_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/obstacle_pressure.png')
    plt.close()

    # Plot total pressure
    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], total_pressure, label='Presión total', color='green', linestyle='--')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Presión [N/m]')
    if use_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/total_pressure.png')
    plt.close()


def plot_temperature_over_time(df_pressure):
    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['temperature'], label='Temperatura', color='orange')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Temperatura [K]')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/temperature_over_time.png')
    plt.show()


def main():
    directory = sys.argv[1]
    df_pressure, df_obstacle_collision, df_particles = parse_simulation_file(directory)
    print(df_pressure)
    print(df_particles)
    print(df_obstacle_collision)
    os.makedirs('observables', exist_ok=True)
    plot_pressure_over_time(df_pressure, use_log_scale=True)
    plot_individual_pressures(df_pressure, use_log_scale=True)
    plot_temperature_over_time(df_pressure)
    plot_collisions_over_time(df_obstacle_collision)

if __name__ == "__main__":
    main();

