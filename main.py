import threading
from simulation import HiveSimulation

def main():
    simulation = HiveSimulation()
    
    def run_sim():
        simulation.run_simulation(max_cycles=100)
    
    sim_thread = threading.Thread(target=run_sim)
    sim_thread.start()
    
    try:
        while sim_thread.is_alive():
            cmd = input("\nEnter command (s: stats, q: quit): ").strip().lower()
            if cmd == 's':
                stats = simulation.get_statistics()
                print("\nCurrent Statistics:")
                for key, value in stats.items():
                    if isinstance(value, dict):
                        print(f"{key}:")
                        for k, v in value.items():
                            print(f"  {k}: {v}")
                    else:
                        print(f"{key}: {value}")
            elif cmd == 'q':
                print("Stopping simulation...")
                simulation.running = False
                break
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        simulation.running = False
    
    sim_thread.join()
    print("Simulation ended.")

if __name__ == "__main__":
    main()