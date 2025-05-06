import numpy as np
import matplotlib.pyplot as plt
import simpy


def customer(env, name, server, arrival_rate, service_rate):
    """Customer process: arrives, waits, gets served, and leaves"""
    arrival_time = env.now
    print(f"{name} arrived at {arrival_time:.2f}")

    with server.request() as req:
        # Wait until it's our turn
        yield req

        # Calculate waiting time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        print(f"{name} waited {wait_time:.2f} units and started service at {env.now:.2f}")

        # Service time (exponentially distributed)
        service_time = np.random.exponential(1 / service_rate)
        yield env.timeout(service_time)

        # Departure
        print(f"{name} finished at {env.now:.2f} (service took {service_time:.2f} units)")

        # Track total time in system
        system_times.append(env.now - arrival_time)


def customer_generator(env, server, arrival_rate, service_rate):
    """Generates customers randomly according to exponential interarrival times"""
    i = 0
    while True:
        # Wait for next customer
        interarrival_time = np.random.exponential(1 / arrival_rate)
        yield env.timeout(interarrival_time)

        # Create customer
        i += 1
        env.process(customer(env, f'Customer {i}', server, arrival_rate, service_rate))


def run_mm1_simulation(arrival_rate, service_rate, simulation_time):
    """Run a complete M/M/1 queue simulation"""
    global wait_times, system_times
    wait_times = []
    system_times = []

    # Create environment and server
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)

    # Start processes
    env.process(customer_generator(env, server, arrival_rate, service_rate))

    # Run simulation
    env.run(until=simulation_time)

    # Calculate theoretical results
    rho = arrival_rate / service_rate
    theoretical_avg_system_time = 1 / (service_rate - arrival_rate)
    theoretical_avg_wait_time = rho / (service_rate - arrival_rate)

    # Print results
    print("\nSimulation Results:")
    print(f"Traffic intensity (ρ): {rho:.2f}")
    print(f"Average time in system (simulated): {np.mean(system_times):.2f}")
    print(f"Average time in system (theoretical): {theoretical_avg_system_time:.2f}")
    print(f"Average wait time (simulated): {np.mean(wait_times):.2f}")
    print(f"Average wait time (theoretical): {theoretical_avg_wait_time:.2f}")

    # Plot results
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.hist(wait_times, bins=20, alpha=0.7)
    plt.axvline(np.mean(wait_times), color='r', linestyle='dashed', linewidth=1)
    plt.title('Wait Time Distribution')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.hist(system_times, bins=20, alpha=0.7)
    plt.axvline(np.mean(system_times), color='r', linestyle='dashed', linewidth=1)
    plt.title('System Time Distribution')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()


# Parameters
arrival_rate = 3  # customers per time unit
service_rate = 4  # customers per time unit
simulation_time = 100  # time units

# Run simulation
run_mm1_simulation(arrival_rate, service_rate, simulation_time).

