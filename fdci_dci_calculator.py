import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd  # Make sure to import pandas
import json  # For reading the JSON file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io  # For saving the plot as a buffer

# Function to load CPI data from an external JSON file
def load_cpi_data():
    with open('cpi_database.json', 'r') as f:
        cpi_data = json.load(f)
    return cpi_data

# Function to load Material Prices from an external JSON file
def load_material_prices(material_type):
    if material_type == "steel":
        with open('steel_prices.json', 'r') as f:
            material_prices = json.load(f)
    elif material_type == "wood":
        with open('wood_prices.json', 'r') as f:
            material_prices = json.load(f)
    elif material_type == "concrete":
        with open('concrete_prices.json', 'r') as f:
            material_prices = json.load(f)
    else:
        raise ValueError("Invalid material type")
    return material_prices

# Function to display the results in a table
def display_table(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values):
    data = {
        "Year": years,
        "FDCI (No Inflation Adjustment)": fdci_values_no_inflation,
        "FDCI (With Inflation Adjustment)": fdci_values_with_inflation,
        "DCI": dci_values
    }
    df = pd.DataFrame(data)
    st.write(df)

# Function to calculate FDCI and DCI for each phase
def calculate_indices(num_phases, material_prices, reuse_factors, material_requirements, cpis, years):
    fdci_values_no_inflation = []
    fdci_values_with_inflation = []
    dci_values = []
    material_from_previous = material_requirements[0]  # Initial material quantity for Phase 1
    
    for i in range(num_phases):
        cost = material_prices[i]
        reuse_factor = reuse_factors[i]
        material_required = material_requirements[i]
        current_cpi = cpis[i]
        current_year = years[i]
        
        reused_material = material_from_previous * reuse_factor / 100
        procured_material = material_required - reused_material
        
        fdci_no_inflation = reused_material / (reused_material + procured_material * cost)
        fdci_values_no_inflation.append(fdci_no_inflation)
        
        past_cpi = cpis[0]
        adjusted_cost = cost * (current_cpi / past_cpi)
        fdci_with_inflation = reused_material / (reused_material + procured_material * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        dci = reused_material / (reused_material + procured_material * cost)
        dci_values.append(dci)
        
        material_from_previous = reused_material

    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values

# Function to save the plot to a BytesIO buffer
def save_plot_to_buffer(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Function to plot the FDCI and DCI graphs
def plot_graphs(phases, fdci_values_no_inflation, fdci_values_with_inflation, dci_values):
    # Plot FDCI with both adjusted and non-adjusted for inflation
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(phases, fdci_values_no_inflation, label="FDCI (No Inflation Adjustment)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax1.plot(phases, fdci_values_with_inflation, label="FDCI (With Inflation Adjustment)", marker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    ax1.set_xlabel('Phase', fontsize=12)
    ax1.set_ylabel('FDCI', fontsize=12)
    ax1.set_title('FDCI Comparison: Inflation Adjusted vs. Non-Adjusted', fontsize=14)
    ax1.grid(True)
    ax1.legend(title="FDCI", fontsize=10)
    
    # Plot DCI
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(phases, dci_values, label="DCI", marker='o', linestyle='-', color='red', linewidth=2, markersize=8)
    ax2.set_xlabel('Phase', fontsize=12)
    ax2.set_ylabel('DCI', fontsize=12)
    ax2.set_title('DCI Across Phases', fontsize=14)
    ax2.grid(True)
    ax2.legend(title="DCI", fontsize=10)

    # Plot FDCI and DCI together
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(phases, fdci_values_no_inflation, label="FDCI (No Inflation Adjustment)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax3.plot(phases, dci_values, label="DCI", marker='o', linestyle='-', color='red', linewidth=2, markersize=8)
    ax3.set_xlabel('Phase', fontsize=12)
    ax3.set_ylabel('Value', fontsize=12)
    ax3.set_title('FDCI and DCI Comparison', fontsize=14)
    ax3.grid(True)
    ax3.legend(title="Comparison", fontsize=10)

    return fig1, fig2, fig3

# Streamlit UI for inputs
def app():
    st.title("FDCI and DCI Calculator")

    # Load CPI data from the external JSON file
    cpi_database = load_cpi_data()

    # Allow user to select the material (steel, wood, or concrete)
    material_type = st.selectbox("Select Material for Calculation", ["steel", "wood", "concrete"])

    # Load material prices from the selected material type
    material_prices_data = load_material_prices(material_type)

    num_phases = st.number_input("Enter number of phases", min_value=1, max_value=20, value=3)
    
    # Ask the user if they want to use the default CPI database or manually input CPIs
    use_cpi_database = st.checkbox("Use default CPI database (1900-2025)")
    
    # If using CPI database, fill in the CPIs automatically; otherwise, allow manual input
    cpis = []
    for i in range(num_phases):
        if use_cpi_database:
            # Allow the user to select a year for each phase and use the CPI from the database
            year = st.number_input(f"Select Year for Phase {i+1} (1900-2025)", min_value=1900, max_value=2025, value=2022)
            cpis.append(cpi_database.get(str(year), 100))  # Default to 100 if CPI is not available for the selected year
        else:
            # Manually input CPI
            cpis.append(st.number_input(f"Enter CPI for Phase {i+1}", min_value=0.0, value=100.0))

    # Ask the user if they want to use the material price database or manually input values
    use_material_price_database = st.checkbox(f"Use default {material_type.capitalize()} Price database (1900-2025)")

    material_prices = []
    for i in range(num_phases):
        if use_material_price_database:
            # Allow the user to select a year and use the material price from the database
            year = st.number_input(f"Select Year for Phase {i+1} {material_type.capitalize()} Price (1900-2025)", min_value=1900, max_value=2025, value=2022)
            # Get material price for the selected year from the database
            price = material_prices_data.get(str(year), 500)  # Default to 500 if year is not found
            material_prices.append(price)
        else:
            # Manually input material price
            material_prices.append(st.number_input(f"Enter {material_type.capitalize()} Price for Phase {i+1} (USD per unit)", min_value=0.0, value=500.0))

    # Display a recap table for CPI and Material Prices for each phase
    recap_data = {
        "Phase": [f"Phase {i+1}" for i in range(num_phases)],
        "Year": [str(year) for year in range(2022, 2022 + num_phases)],
        "CPI": cpis,
        f"{material_type.capitalize()} Price (USD)": material_prices
    }
    recap_df = pd.DataFrame(recap_data)
    st.write("### Recap Table: CPI and Material Prices for Each Phase")
    st.write(recap_df)

    # Gather other inputs for the material requirements and reuse factors
    material_requirement = [st.number_input(f"Enter initial quantity of {material_type} for Phase 1 (tons)", min_value=1, value=1000)]
    reuse_factors = [st.number_input(f"Phase 1 - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0)]
    years = [2022]  # Default to the current year

    # Gather the rest of the data for phases
    for i in range(1, num_phases):
        material_requirement.append(st.number_input(f"Phase {i+1} - Material Requirement (tons)", min_value=1, value=1000))
        reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))
        years.append(st.number_input(f"Phase {i+1} - Year", min_value=1900, max_value=2025, value=2022))

    # Start the calculation and display results
    if st.button("Start Calculation"):
        fdci_values_no_inflation, fdci_values_with_inflation, dci_values = calculate_indices(num_phases, material_prices, reuse_factors, material_requirement, cpis, years)
        
        # Display results in table
        display_table(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values)
        
        # Plot the graphs
        fig1, fig2, fig3 = plot_graphs(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values)
        
        # Display the plots in Streamlit
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)

        # Save plot button (optional)
        if st.button("Save Plot as PNG"):
            buf1 = save_plot_to_buffer(fig1)
            buf2 = save_plot_to_buffer(fig2)
            buf3 = save_plot_to_buffer(fig3)
            
            st.download_button(
                label="Download FDCI Plot (PNG)",
                data=buf1,
                file_name="fdci_comparison.png",
                mime="image/png"
            )

            st.download_button(
                label="Download DCI Plot (PNG)",
                data=buf2,
                file_name="dci_comparison.png",
                mime="image/png"
            )

            st.download_button(
                label="Download FDCI and DCI Comparison Plot (PNG)",
                data=buf3,
                file_name="fdci_dci_comparison.png",
                mime="image/png"
            )

# Run the Streamlit app
if __name__ == "__main__":
    app()
