import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

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

# Function to plot the graph
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

# GUI function to start calculations
def start_calculation():
    try:
        # Gather input from the user
        num_phases = int(entry_num_phases.get())
        steel_prices = [float(entry_steel_price[i].get()) for i in range(num_phases)]
        reuse_factors = [float(entry_reuse_factor[i].get()) for i in range(num_phases)]
        years = [int(entry_year[i].get()) for i in range(num_phases)]
        cpis = [float(entry_cpi[i].get()) for i in range(num_phases)]
        inflation_adjustment = var_inflation.get()

        # Call the function to calculate FDCI and DCI
        fdci_values, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years, inflation_adjustment)

        # Display the results
        messagebox.showinfo("Calculation Completed", "Calculation complete! Click 'Plot' to view the graph.")

        # Plot the graph
        plot_type = combo_plot_type.get()
        plot_graph(years, fdci_values, dci_values, plot_type)

        # Enable the reset button after the calculation is completed
        reset_button.config(state=tk.NORMAL)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please ensure all inputs are correct.")

# GUI function to reset inputs
def reset_inputs():
    # Clear all input fields
    entry_num_phases.delete(0, tk.END)
    for i in range(int(entry_num_phases.get())):
        entry_steel_price[i].delete(0, tk.END)
        entry_reuse_factor[i].delete(0, tk.END)
        entry_year[i].delete(0, tk.END)
        entry_cpi[i].delete(0, tk.END)

    # Disable the reset button after resetting
    reset_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("FDCI and DCI Calculator")

# Create and place widgets in the window
tk.Label(root, text="Number of Phases:").grid(row=0, column=0, pady=5)
entry_num_phases = tk.Entry(root)
entry_num_phases.grid(row=0, column=1, pady=5)

# Create dynamic input fields for steel prices, reuse factors, years, and CPI
entry_steel_price = []
entry_reuse_factor = []
entry_year = []
entry_cpi = []

def create_phase_inputs(num_phases):
    for i in range(num_phases):
        tk.Label(root, text=f"Phase {i+1} Steel Price:").grid(row=i+1, column=0)
        entry_steel_price.append(tk.Entry(root))
        entry_steel_price[i].grid(row=i+1, column=1, pady=5)

        tk.Label(root, text=f"Phase {i+1} Reuse Factor:").grid(row=i+1, column=2)
        entry_reuse_factor.append(tk.Entry(root))
        entry_reuse_factor[i].grid(row=i+1, column=3, pady=5)

        tk.Label(root, text=f"Phase {i+1} Year:").grid(row=i+1, column=4)
        entry_year.append(tk.Entry(root))
        entry_year[i].grid(row=i+1, column=5, pady=5)

        tk.Label(root, text=f"Phase {i+1} CPI:").grid(row=i+1, column=6)
        entry_cpi.append(tk.Entry(root))
        entry_cpi[i].grid(row=i+1, column=7, pady=5)

# Submit button to start calculations
submit_button = tk.Button(root, text="Start Calculation", command=start_calculation)
submit_button.grid(row=num_phases+1, column=0, columnspan=2, pady=10)

# ComboBox for selecting plot type (FDCI or DCI)
tk.Label(root, text="Select Plot Type:").grid(row=num_phases+2, column=0, pady=5)
combo_plot_type = tk.Combobox(root, values=["FDCI", "DCI"])
combo_plot_type.grid(row=num_phases+2, column=1)

# Checkbox for inflation adjustment
var_inflation = tk.BooleanVar()
inflation_checkbox = tk.Checkbutton(root, text="Adjust for Inflation", variable=var_inflation)
inflation_checkbox.grid(row=num_phases+3, column=0, columnspan=2)

# Reset button to clear inputs
reset_button = tk.Button(root, text="Reset", command=reset_inputs, state=tk.DISABLED)
reset_button.grid(row=num_phases+4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
