import time
import random
import numpy as np
from track_classifier import GPSClassifier

def get_raw_gps_packet():
    # Simulates raw data coming from a GPS location function
    return {
        "lat": random.uniform(-15, 15),
        "lon": random.uniform(-5, 5),
        "unit": "meters"
    }

def run_simulation():
    # Setup
    try:
        engine = GPSClassifier("configuration_file.json")
    except FileNotFoundError:
        print("Error: Please create a configuration_file.json first.")
        return

    print(f"{'Source':<12} | {'Coord (X,Y)':<15} | {'Dist_A':>8} | {'Dist_B':>8} | {'Status'}")
    print("-" * 70)

    # Part 1: Linear Motion Simulation (Left to Right)
    sim_config = engine.config.get('simulation', {})
    x_range = np.arange(sim_config.get('start_x'), sim_config.get('end_x'), sim_config.get('step_size'))

    for x in x_range:
        engine.update_position(x, 0.0)
        status = engine.classify()
        print(f"{'Linear_Sim':<12} | {f'({x:0.1f}, 0.0)':<15} | {engine.dist_a():8.1f} | {engine.dist_b():8.1f} | {status}")
        time.sleep(0.05)

    print("-" * 70)

    # Part 2: Real-time GPS Simulation
    for _ in range(5):
        raw_data = get_raw_gps_packet()
        engine.update_position(raw_data['lat'], raw_data['lon'])

        # Pre-format coordinates
        coord_str = f"({raw_data['lat']:0.1f}, {raw_data['lon']:0.1f})"

        print(f"{'Hardware_GPS':<12} | {coord_str:<15} | "
              f"{engine.dist_a():8.1f} | {engine.dist_b():8.1f} | {engine.classify()}")
        time.sleep(0.5)

if __name__ == "__main__":
    run_simulation()
