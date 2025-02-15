import numpy as np

# Function to calculate FDCI and DCI for each phase
def calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, inflation_adjustment=False):
    fdci_values = []
    dci_values = []
    mass_remaining = steel_requirement
    
    for i in range(num_phases):
        # User-defined steel price and reuse factor for each phase
        cost = steel_prices[i]
        reuse_factor = reuse_factors[i]
        
        # Adjust for inflation if requested
        if inflation_adjustment:
            cost = cost * (cpi_values[2025] / cpi_values[years[i]])

        # FDCI Calculation
        steel_from_previous = mass_remaining * reuse_factor
        steel_from_market = mass_remaining - steel_from_previous
        fdci = (steel_from_previous * reuse_factor) / (steel_from_previous + steel_from_market * cost)
        fdci_values.append(fdci)
        
        # DCI Calculation
        dci = (steel_from_previous * reuse_factor) / (steel_from_previous + steel_from_market * cost)
        dci_values.append(dci)
        
        # Update mass for the next phase (steel used from previous phase)
        mass_remaining = steel_from_previous

    return fdci_values, dci_values

# User input for the number of phases and parameters
num_phases = int(input("Enter the number of phases: "))
steel_prices = []
reuse_factors = []

# Collecting user input for steel prices and reuse factors
for i in range(num_phases):
    price = float(input(f"Enter the steel price for phase {i+1} in USD per ton: "))
    reuse = float(input(f"Enter the reuse factor for phase {i+1} (between 0 and 1): "))
    steel_prices.append(price)
    reuse_factors.append(reuse)

steel_requirement = 1000  # Fixed steel requirement per phase

# Optional inflation adjustment (add inflation data if needed)
inflation_adjustment = input("Would you like to adjust for inflation? (y/n): ").lower() == 'y'

# Call the calculation function
fdci_values, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, inflation_adjustment)

# Display results
print("\nFDCI values per phase:")
for i, fdci in enumerate(fdci_values):
    print(f"Phase {i+1}: FDCI = {fdci:.4f}")

print("\nDCI values per phase:")
for i, dci in enumerate(dci_values):
    print(f"Phase {i+1}: DCI = {dci:.4f}")
