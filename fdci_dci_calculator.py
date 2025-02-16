import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed the plot inside Tkinter

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

# Function to plot the graph inside the Tkinter interface
def plot_graph(phases, fdci_values, dci_values, plot_type='FDCI'):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot based on user's choice: FDCI, DCI, or both
    if plot_type == 'FDCI' or plot_type == 'Both':
        ax.plot(phases, fdci_values, label="FDCI", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    if plot_type == 'DCI' or plot_type == 'Both':
        ax.plot(phases, dci_values, label="DCI", marker='o', linestyle='-', color='red', linewidth=2, markersize=8)

    ax.set_xlabel('Phase', fontsize=14)
    ax.set_ylabel('Circularity Index (FDCI & DCI)', fontsize=14)
    ax.set_title(f'{plot_type} Comparison Across Phases', fontsize=16)
    ax.grid(True)
    ax.legend(title="Index Type", fontsize=12)

    # Embed the plot in the Tkinter interface
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)  # Create a canvas to embed the figure
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return fig  # Return the figure to save later

# Function to save the plot as PNG
def save_plot_as_png(fig):
    try:
        fig.savefig("fdci_dci_plot.png")
        messagebox.showinfo("Saved", "Plot has been saved as 'fdci_dci_plot.png'.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving plot: {str(e)}")

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
        steel_requirement = float(entry_steel_requirement.get())  # Get user-defined steel requirement

        # Call the function to calculate FDCI and DCI
        fdci_values, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years, inflation_adjustment)

        # Display the results
        messagebox.showinfo("Calculation Completed", "Calculation complete! Click 'Plot' to view the graph.")

        # Plot the graph
        plot_type = combo_plot_type.get()
        fig = plot_graph(years, fdci_values, dci_values, plot_type)

        # Enable the reset and save buttons after the calculation is completed
        reset_button.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL, command=lambda: save_plot_as_png(fig))

    except ValueError:
        messagebox.showerror("Invalid Input", "Please ensure all inputs are correct.")

# GUI function to reset inputs
def reset_inputs():
    # Clear all input fields
    entry_num_phases.delete(0, tk.END)
    entry_steel_requirement.delete(0, tk.END)
    for i in range(int(entry_num_phases.get())):
        entry_steel_price[i].delete(0, tk.END)
        entry_reuse_factor[i].delete(0, tk.END)
        entry_year[i].delete(0, tk.END)
        entry_cpi[i].delete(0, tk.END)

    # Disable the reset and save buttons after resetting
    reset_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("FDCI and DCI Calculator")

# Function to create input fields dynamically based on number of phases
def create_phase_inputs():
    num_phases = int(entry_num_phases.get())  # Get number of phases from the user input

    # Create dynamic input fields for steel prices, reuse factors, years, and CPI
    global entry_steel_price, entry_reuse_factor, entry_year, entry_cpi
    entry_steel_price = []
    entry_reuse_factor = []
    entry_year = []
    entry_cpi = []
    
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

    # ComboBox for selecting plot type (FDCI or DCI or Both)
    tk.Label(root, text="Select Plot Type:").grid(row=num_phases+2, column=0, pady=5)
    global combo_plot_type
    combo_plot_type = ttk.Combobox(root, values=["FDCI", "DCI", "Both"])
    combo_plot_type.grid(row=num_phases+2, column=1)

    # Checkbox for inflation adjustment
    global var_inflation
    var_inflation = tk.BooleanVar()
    inflation_checkbox = tk.Checkbutton(root, text="Adjust for Inflation", variable=var_inflation)
    inflation_checkbox.grid(row=num_phases+3, column=0, columnspan=2)

    # Entry for steel requirement
    tk.Label(root, text="Steel Requirement (tons per phase):").grid(row=num_phases+4, column=0, pady=5)
    global entry_steel_requirement
    entry_steel_requirement = tk.Entry(root)
    entry_steel_requirement.grid(row=num_phases+4, column=1, pady=5)

    # Reset and save buttons
    reset_button.grid(row=num_phases+5, column=0, columnspan=2, pady=10)
    save_button.grid(row=num_phases+6, column=0, columnspan=2, pady=10)

# Create the input fields for number of phases
tk.Label(root, text="Number of Phases:").grid(row=0, column=0, pady=5)
entry_num_phases = tk.Entry(root)
entry_num_phases.grid(row=0, column=1, pady=5)

# Add space between Generate Phase inputs and phase input fields
generate_button = tk.Button(root, text="Generate Phase Inputs", command=create_phase_inputs)
generate_button.grid(row=1, column=0, columnspan=2, pady=30)

# Frame for plotting graph
frame_graph = tk.Frame(root)
frame_graph.grid(row=0, column=2, rowspan=10, padx=20)

# Save button
save_button = tk.Button(root, text="Save Plot as PNG", state=tk.DISABLED)

# Start the Tkinter event loop
root.mainloop()
