import numpy as np
import simpy
import matplotlib.pyplot as plt


def ential(param):
    pass


def customer_arrivals(env, service_desk, arrival_rate, service_rate):
    """Generate customer arrivals according to Poisson process."""
    customer_id = 0

    # Run indefinitely
    while True:
        # Generate time until next arrival (exponentially distributed)
        interarrival_time = np.random.expon


        ential(1.0 / arrival_rate)

        # Wait until next customer arrives
        yield env.timeout(interarrival_time)

        # Create new customer
        customer_id += 1
        env.process(customer(env, f"Customer {customer_id}", service_desk, service_rate))


def customer(env, name, service_desk, service_rate):
    """Customer process: arrives, waits for service, and leaves."""
    arrival_time = env.now

    # Request service
    with service_desk.request() as request:
        # Wait until it's our turn
        yield request

        wait_time = env.now - arrival_time
        waiting_times.append(wait_time)

        # Generate service time (also often exponentially distributed)
        service_time = np.random.exponential(1.0 / service_rate)

        # Service is being performed
        yield env.timeout(service_time)


# Simulation parameters
arrival_rate = 5.0  # customers per time unit
service_rate = 6.0  # customers per time unit
sim_time = 100  # simulation time units
num_servers = 1  # number of service points

# Set up and run simulation
waiting_times = []
env = simpy.Environment()
service_desk = simpy.Resource(env, capacity=num_servers)
env.process(customer_arrivals(env, service_desk, arrival_rate, service_rate))
env.run(until=sim_time)

# Plot results
plt.hist(waiting_times, bins=20)
plt.title("Customer Waiting Times")
plt.xlabel("Time")
plt.ylabel("Number of Customers")
plt.show()

print(f"Average waiting time: {np.mean(waiting_times):.2f} time units")
print(f"Maximum waiting time: {np.max(waiting_times):.2f} time units")