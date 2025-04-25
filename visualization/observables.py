import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

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
            # temperature = float(lines[i].strip())
            # i += 1
            firstTimeCollisions = int(lines[i].strip())
            i += 1
            totalCollisions = int(lines[i].strip())
            i += 1
            # pressure_data.append([t, wallPressure, obstaclePressure, temperature])
            pressure_data.append([t, wallPressure, obstaclePressure])

            collision_data.append([t, firstTimeCollisions, totalCollisions])
            for _ in range(n):
                x, y, vx, vy, r, m = map(float, lines[i].strip().split())
                particle_data.append([t, x, y, vx, vy, r, m])
                i += 1

    # df_pressure = pd.DataFrame(pressure_data, columns=['time', 'wallPressure', 'obstaclePressure', 'temperature'])
    df_pressure = pd.DataFrame(pressure_data, columns=['time', 'wallPressure', 'obstaclePressure'])
    df_obstacle_collisions = pd.DataFrame(collision_data, columns=['time', 'firstTimeCollisions', 'totalCollisions'])
    df_particles = pd.DataFrame(particle_data, columns=['time', 'x', 'y', 'vx', 'vy', 'radius', 'mass'])
    return df_pressure, df_obstacle_collisions, df_particles

def parse_multiple_simulation_files(files):
    df_pressure_list = []
    df_obstacle_collisions_list = []
    df_particles_list = []

    for f in files:
        pressure, collisions, particles = parse_simulation_file(f)
        pressure['simulation'] = f
        collisions['simulation'] = f
        particles['simulation'] = f
        df_pressure_list.append(pressure)
        df_obstacle_collisions_list.append(collisions)
        df_particles_list.append(particles)

    df_pressure = pd.concat(df_pressure_list, ignore_index=True)
    df_obstacle_collisions = pd.concat(df_obstacle_collisions_list, ignore_index=True)
    df_particles = pd.concat(df_particles_list, ignore_index=True)

    return df_pressure, df_obstacle_collisions, df_particles


def plot_collisions_over_time(df_collisions):

    df_by_sim = df_collisions.groupby('simulation')

    fig_first_collision, ax_first_collision = plt.subplots(figsize=(10, 6))
    fig_total_collisions, ax_total_collisions = plt.subplots(figsize=(10, 6))

    for sim, group in df_by_sim:
        ax_first_collision.plot(group['time'], group['firstTimeCollisions'], label=f'v = {sim.split("-")[2][:-4]} m/s', alpha=0.5)
        ax_total_collisions.plot(group['time'], group['totalCollisions'], label=f'v = {sim.split("-")[2][:-4]} m/s', alpha=0.5)
    
    ax_first_collision.set_xlabel('Tiempo [s]', fontsize=14)
    ax_first_collision.set_ylabel('Número de colisiones (primeras)', fontsize=14)
    ax_first_collision.legend()
    ax_first_collision.grid(True)
    fig_first_collision.tight_layout()
    fig_first_collision.savefig('observables/collisions_over_time.png')
    fig_first_collision.show()

    ax_total_collisions.set_xlabel('Tiempo [s]', fontsize=14)
    ax_total_collisions.set_ylabel('Número de colisiones (acumuladas)', fontsize=14)
    ax_total_collisions.legend()    
    ax_total_collisions.grid(True)
    fig_total_collisions.tight_layout()
    fig_total_collisions.savefig('observables/total_collisions_over_time.png')
    fig_total_collisions.show()

def calculate_collision_rate(df_collisions, df_pressure):
    total_time = df_collisions['time'].iloc[-1]
    total_collisions = df_collisions['totalCollisions'].iloc[-1]
    collision_rate = total_collisions / total_time
    temperature = df_pressure['temperature'].mean()
    print(f"Tasa de colisión: {collision_rate:.2f} collision/s a Temperatura: {temperature:.2f} K")


def plot_collision_rate_over_temperature(df_collisions, df_particles):
    
    df_by_sim = df_collisions.groupby('simulation')
    collision_rates = []
    
    mass = df_particles.groupby('simulation')['mass'].mean()

    df_particles['v_squared'] = df_particles['vx']**2 + df_particles['vy']**2
    v_squared_stats = df_particles.groupby('simulation')['v_squared'].agg(['mean', 'std']).reset_index()
    temperature = 0.5 * mass.values * v_squared_stats['mean'] 

    for sim, group in df_by_sim:
        total_time = group['time'].iloc[-1]
        total_collisions = group['totalCollisions'].iloc[-1]
        collision_rate = total_collisions / total_time
        collision_rates.append(collision_rate)

    plt.figure(figsize=(10, 6))
    plt.plot(temperature, collision_rates, 'o', label='Tasa de colisiones')
    plt.xlabel('Temperatura', fontsize=14)
    plt.ylabel('Tasa de colisiones [collision/s]', fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('observables/collision_rate_over_temperature.png')
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



def plot_pressure_over_temperature(df_pressure, df_particles):

    mass = df_particles.groupby('simulation')['mass'].mean()

    df_particles['v_squared'] = df_particles['vx']**2 + df_particles['vy']**2
    v_squared_stats = df_particles.groupby('simulation')['v_squared'].agg(['mean', 'std']).reset_index()
    temperature = 0.5 * mass.values * v_squared_stats['mean'] 

    pressure_stats = df_pressure.groupby('simulation').agg({
        'wallPressure': ['mean', 'std'],
        'obstaclePressure': ['mean', 'std']
    })

    pressure_stats.columns = ['wall_mean', 'wall_std', 'obstacle_mean', 'obstacle_std']
    pressure_stats = pressure_stats.reset_index()

    pressure_stats['system_pressure'] = pressure_stats['wall_mean'] + pressure_stats['obstacle_mean']
    pressure_stats['pressure_error'] = np.sqrt(pressure_stats['wall_std']**2 + pressure_stats['obstacle_std']**2)

    plt.figure(figsize=(10, 6))

    plt.errorbar(
        temperature,
        pressure_stats['system_pressure'],
        yerr=pressure_stats['pressure_error'],
        fmt='o',
        color='blue',
        label='Presión vs Temperatura'
    )

    ax = plt.gca()  
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.xlabel('Temperatura', fontsize=14)
    plt.ylabel('Presión [N/m²]', fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('observables/pressure_over_temperature.png')
    plt.show()

def plot_pressure_over_time(df_pressure, name, use_log_scale=False):
    total_pressure = df_pressure['wallPressure'] + df_pressure['obstaclePressure']

    # Equilibrium value: average of the last 10% of total pressure
    equilibrium_pressure = total_pressure.iloc[int(0.9 * len(total_pressure)):].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(df_pressure['time'], df_pressure['wallPressure'], label='Presión Pared', color='blue')
    plt.plot(df_pressure['time'], df_pressure['obstaclePressure'], label='Presión Obstaculo', color='red')
    plt.plot(df_pressure['time'], total_pressure, label='Presión Total', color='green', linestyle='--')

    # Draw equilibrium line
    plt.axhline(equilibrium_pressure, color='gray', linestyle=':', label=f'Equilibrio ≈ {equilibrium_pressure:.0f} N/m')

    plt.xlabel('Tiempo [s]', fontsize=14)
    plt.ylabel('Presión [N/m]', fontsize=14)
    if use_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'observables/pressure_over_time_{name}.png')
    plt.show()

def plot_pressures_over_time(df_pressure, use_log_scale=False):
    df_by_sim = df_pressure.groupby('simulation')

    for sim, group in df_by_sim:
        v_val = sim.split("-")[2][:-4]
        plot_pressure_over_time(group, sim, True)


def main():

    if len(sys.argv) == 1:
        return print("Usage: python observables.py <directory>")

    elif len(sys.argv) == 2:
        directory = sys.argv[1]
        df_pressure, df_obstacle_collision, df_particles = parse_simulation_file(directory)
    
    else:
        files = sys.argv[1:]
        df_pressure, df_obstacle_collision, df_particles = parse_multiple_simulation_files(files)

    # print(df_pressure)
    # print(df_particles)
    # print(df_obstacle_collision)
    # os.makedirs('observables', exist_ok=True)
    plot_pressures_over_time(df_pressure, True)
    # plot_individual_pressures(df_pressure, use_log_scale=True)
    # plot_temperature_over_time(df_pressure)
    # plot_collisions_over_time(df_obstacle_collision)
    # plot_collision_rate_over_temperature(df_obstacle_collision, df_particles)
    # plot_pressure_over_temperature(df_pressure, df_particles)

if __name__ == "__main__":
    main();

