import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress


def parse_big_particle_positions(filename):
    times = []
    positions = []

    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    N = int(lines[idx])
    idx += 1

    while idx < len(lines):
        t = float(lines[idx])
        idx += 6  # Skip time, wall_pressure, obstacle_pressure

        parts = lines[idx].split()
        x, y = float(parts[0]), float(parts[1])
        positions.append((x, y))
        times.append(t)
        idx += N


    return np.array(times), np.array(positions)

def compute_msd(times, positions, start_time=0.5, interval=0.2, max_time=None):
    if max_time is None:
        max_time = times[-1]

    dcm_times = []
    dcm_values = []
    dcm_stds=[]
    t0 = start_time
    while t0 + interval <= max_time:
        i = np.searchsorted(times, t0, side='left')
        j = np.searchsorted(times, t0 + interval, side='left')

        if i < len(times) and j < len(times):
            r0 = positions[i]
            r1 = positions[j]
            displacement = r1 - r0
            squared_displacement = np.average(displacement ** 2)

            dcm_times.append(t0)
            dcm_values.append(squared_displacement)
            dcm_stds.append(np.std(displacement**2))
        t0 += interval

    return np.array(dcm_times), np.array(dcm_values),np.array(dcm_stds)

"""
In the compute_dcm function, the goal is to align the time points from multiple simulation runs to a common set of 
evenly spaced time points (common_times). This is necessary because the time points in each simulation run (sorted_times)
may not match exactly. Interpolation is used to estimate the x-coordinates (sorted_x) at these common time points.
"""
def compute_dcm(times, all_positions, start_time=0.05, num_points=100):
    """
    Computes the average Mean Squared Displacement (MSD) and its standard deviation over multiple simulation runs.
    """
    num_runs = len(times)
    if not num_runs == len(all_positions):
        raise ValueError("The number of time and position arrays must be the same.")

    min_overall_time = float('inf')
    max_overall_time = float('-inf')

    for time_run in times:
        if time_run.size > 0:
            min_overall_time = min(min_overall_time, np.min(time_run))
            max_overall_time = max(max_overall_time, np.max(time_run))

    if min_overall_time == float('inf'):
        return pd.DataFrame({'time': [], 'average_msd': [], 'std_deviation': []})

    effective_start_time = start_time if start_time >= min_overall_time else min_overall_time
    common_times = np.linspace(effective_start_time, max_overall_time, num_points)
    all_squared_displacements = np.zeros((num_runs, num_points))

    for i in range(num_runs):
        time_points = times[i]
        positions = all_positions[i]

        if not len(time_points) == len(positions):
            raise ValueError(f"Time and position arrays for run {i+1} must have the same length.")

        positions_array = np.array(positions)
        if positions_array.ndim != 2 or positions_array.shape[1] != 2:
            raise ValueError(f"Position array for run {i+1} must be 2-dimensional with (x, y) coordinates.")

        x_coords = positions_array[:, 0]
        y_coords = positions_array[:, 1]

        # Ensure time points are sorted for interpolation
        sort_indices = np.argsort(time_points)
        sorted_times = time_points[sort_indices]
        sorted_x = x_coords[sort_indices]
        sorted_y = y_coords[sort_indices]

        # Find initial position (at the first recorded time)
        initial_x = sorted_x[0] if len(sorted_x) > 0 else 0.0
        initial_y = sorted_y[0] if len(sorted_y) > 0 else 0.0

        squared_displacements = np.zeros(num_points)
        if len(sorted_times) > 1:
            interp_x = np.interp(common_times, sorted_times, sorted_x)
            interp_y = np.interp(common_times, sorted_times, sorted_y)
            squared_displacements = (interp_x - initial_x)**2 + (interp_y - initial_y)**2
        elif len(sorted_times) == 1:
            squared_displacements = np.full(num_points, (sorted_x - initial_x)**2 + (sorted_y - initial_y)**2)
        else:
            squared_displacements = np.zeros(num_points)  # If no data points in the run

        all_squared_displacements[i] = squared_displacements

    average_msd_values = np.mean(all_squared_displacements, axis=0)
    std_deviation_values = np.std(all_squared_displacements, axis=0)

    return pd.DataFrame({
        'time': common_times,
        'average_msd': average_msd_values,
        'std_deviation': std_deviation_values
    })


def plot_dcm(average_msd_df):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        average_msd_df['time'],
        average_msd_df['average_msd'],
        yerr=average_msd_df['std_deviation'],
        fmt='o',
        color='#2ca25f',
        ecolor='#99d8c9',
        capsize=4,
    )
    plt.xlabel('Tiempo [s]', fontsize=20)
    plt.ylabel('< DCM > [$m^2$]', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def compute_diffusion_coefficient(average_msd_df):
    times = average_msd_df['time'].values
    dcm = average_msd_df['average_msd'].values

    if len(times) != len(dcm):
        raise ValueError("The lengths of 'time' and 'average_msd' columns must be equal.")
    if len(times) < 2:
        raise ValueError("At least two data points are needed for analysis.")

    # Perform the linear regression
    slope, intercept, r_value, p_value, std_err = linregress(times, dcm)
    # DCM = 4 * D * t
    diffusion_coefficient = slope / 4.0

    return diffusion_coefficient, slope, std_err


if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python dcm.py <simulation_file1> <simulation_file2> ...")
        sys.exit(1)

    filenames = sys.argv[1:]
    all_positions = []
    all_times = []
    for filename in filenames:
        print(f"Processing file: {filename}")
        times, positions = parse_big_particle_positions(filename)
        all_times.append(times)
        all_positions.append(positions)

    average_msd_df = compute_dcm(all_times, all_positions)
    d, slope, std_err = compute_diffusion_coefficient(average_msd_df)
    plot_dcm(average_msd_df)
    print(f"Coeficiente de difusión (D): {d:.1e}")
    print(f"Pendiente: {slope:.1e}")
    print(f"Error std: {std_err:.1e}")
