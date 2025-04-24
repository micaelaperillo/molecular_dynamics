import sys
import matplotlib.pyplot as plt
import numpy as np


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
if __name__=="__main__":
    filename = sys.argv[1]
    times, positions = parse_big_particle_positions(filename)
    filtered_times, msd, stdev = compute_msd(times, positions, start_time=0.5)
    coeffs = np.polyfit(filtered_times, msd, 1)
    slope = coeffs[0]
    D = slope / 4

    plt.errorbar(filtered_times, msd,yerr=stdev, fmt='-o')
    plt.plot(times, np.polyval(coeffs, times), label=f"Fit (D ≈ {D:.2e})", linestyle='--')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('DCM [$m^{2}$]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
