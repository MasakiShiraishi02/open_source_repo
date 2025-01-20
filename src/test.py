from pyqubo import Array, Constraint, Placeholder, solve_qubo
from dimod import ConstrainedQuadraticModel
from dwave.system import LeapHybridCQMSampler

# Problem Parameters
num_shipments = 3
num_trucks = 2
truck_capacity = [100, 200]
truck_cost = [10, 20]
goods_load = [50, 30, 70]

# Define binary variables
X = Array.create('X', shape=(num_shipments, num_trucks, 2*num_shipments), vartype='BINARY')
Y = Array.create('Y', shape=(num_shipments, num_trucks, 2*num_shipments), vartype='BINARY')
Z = Array.create('Z', shape=(num_trucks,), vartype='BINARY')

# Define constraints
constraints = []

# Example Constraint: A transportation request must be served by some truck
for i in range(num_shipments):
    constraints.append(Constraint(
        sum(X[i, j, p] + Y[i, j, p] for j in range(num_trucks) for p in range(2*num_shipments)) == 1,
        label=f"shipment_{i}_served"
    ))

# Objective function
objective = sum(Z[j] * truck_cost[j] for j in range(num_trucks))

# Add constraints to the CQM
cqm = ConstrainedQuadraticModel()
for c in constraints:
    cqm.add_constraint(c)

cqm.set_objective(objective)

# Solve the CQM using D-Wave's hybrid solver
sampler = LeapHybridCQMSampler()
result = sampler.sample_cqm(cqm)

# Display results
for solution, energy in result.data(['sample', 'energy']):
    print(f"Solution: {solution}, Energy: {energy}")
