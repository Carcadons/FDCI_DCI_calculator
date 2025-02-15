import numpy as np
import matplotlib.pyplot as plt

# Function to calculate FDCI and DCI for each phase
def calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years, inflation_adjustment=False):
    fdci_values = []
    dci_values = []
    mass_remaining = steel_requirement
    
    for i in range(num_phases):
        # User-defined steel price, reuse factor, CPI, and year for each phase
        cost = steel_prices[i]
        reuse_factor = reuse_factors[i]
        current_cpi = cpis[i]
        current_year = years[i]
        
        # Adjust for inflation if requested
        if inflation_adjustment:
            # Using the formula: Current Value = Past Value * (Current CPI / Past CPI)
            past_cpi = cpis[0]  # Use the CPI of the first phase (base year)
            cost = cost * (current_cpi / past_cpi)
        
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

# Function to plot the FDCI or DCI graph
def plot_graph(phases, fdci_values, dci_values, plot_type='FDCI'):
    plt.figure(figsize=(14,8))
    if plot_type == 'FDCI':
        plt.plot(phases, fdci_values, label="FDCI", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    elif plot_type == 'DCI':
        plt.plot(phases, dci_values, label="DCI", marker='o', linestyle='-', color='red', linewidth=2, markersize=8)

    plt.xlabel('Phase', fontsize=14)
    plt.ylabel('Circularity Index (FDCI & DCI)', fontsize=14)
    plt.title(f'{plot_type} Comparison Across Phases', fontsize=16)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title="Index Type", fontsize=12)
    plt.tight_layout()
    plt.show()

# User input for the number of phases and parameters
num_phases = int(input("Enter the number of phases: "))
steel_prices = []
reuse_factors = []
years = []
cpis = []

# Collecting user input for steel prices, reuse factors, years, and CPI for each phase
for i in range(num_phases):
    price = float(input(f"Enter the steel price for phase {i+1} in USD per ton: "))
    reuse = float(input(f"Enter the reuse factor for phase {i+1} (between 0 and 1): "))
    year = int(input(f"Enter the year for phase {i+1}: "))
    cpi = float(input(f"Enter the CPI for the year {year} for phase {i+1}: "))
    
    steel_prices.append(price)
    reuse_factors.append(reuse)
    years.append(year)
    cpis.append(cpi)

steel_requirement = 1000  # Fixed steel requirement per phase

# Optional inflation adjustment
inflation_adjustment = input("Would you like to adjust for inflation? (y/n): ").lower() == 'y'

# Call the calculation function
fdci_values, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years, inflation_adjustment)

# Display results
print("\nFDCI values per phase:")
for i, fdci in enumerate(fdci_values):
    print(f"Phase {i+1}: FDCI = {fdci:.4f}")

print("\nDCI values per phase:")
for i, dci in enumerate(dci_values):
    print(f"Phase {i+1}: DCI = {dci:.4f}")

# Ask the user which graph to plot (FDCI or DCI)
plot_type = input("Which graph would you like to plot? (FDCI or DCI): ").upper()
plot_graph(years, fdci_values, dci_values, plot_type)
