import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd  # Import pandas with the alias 'pd'
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot based on user's choice: FDCI, DCI, or both
    if plot_type == 'FDCI' or plot_type == 'Both':
        ax.plot(phases, fdci_values, label="FDCI", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    if plot_type == 'DCI' or plot_type == 'Both':
        ax.plot(phases, dci_values, label="DCI", marker='o', linestyle='-', color='red', linewidth=2, markersize=8)

    ax.set_xlabel('Phase', fontsize=12)
    ax.set_ylabel('Circularity Index (FDCI & DCI)', fontsize=12)
    ax.set_title(f'{plot_type} Comparison Across Phases', fontsize=14)
    ax.grid(True)
    ax.legend(title="Index Type", fontsize=10)

    return fig

# Function to display the results in a table
def display_table(years, fdci_values, dci_values):
    data = {
        "Year": years,
        "FDCI": fdci_values,
        "DCI": dci_values
    }
    df = pd.DataFrame(data)
    st.write(df)

# Streamlit UI for inputs
def app():
    st.title("FDCI and DCI Calculator")

    num_phases = st.number_input("Enter number of phases", min_value=1, max_value=20, value=3)
    
    steel_prices = []
    reuse_factors = []
    years = []
    cpis = []

    for i in range(num_phases):
        steel_prices.append(st.number_input(f"Phase {i+1} - Steel Price (USD per ton)", min_value=0.0, value=500.0))
        reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))
        # Remove the restriction on the year input
        years.append(st.number_input(f"Phase {i+1} - Year", min_value=1, value=2022))  # No lower bound for the year
        cpis.append(st.number_input(f"Phase {i+1} - CPI", min_value=0.0, value=100.0))

    steel_requirement = st.number_input("Enter steel requirement (tons per phase)", min_value=1, value=1000)
    inflation_adjustment = st.checkbox("Adjust for Inflation")

    # Start the calculation and display results
    if st.button("Start Calculation"):
        fdci_values, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years, inflation_adjustment)
        
        # Display results in table
        display_table(years, fdci_values, dci_values)
        
        # Plot the graph
        plot_type = st.selectbox("Select Plot Type", ["FDCI", "DCI", "Both"])
        fig = plot_graph(years, fdci_values, dci_values, plot_type)
        
        # Display plot in Streamlit
        st.pyplot(fig)

        # Save plot button
        if st.button("Save Plot as PNG"):
            fig.savefig("fdci_dci_plot.png")
            st.success("Plot saved as 'fdci_dci_plot.png'.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
