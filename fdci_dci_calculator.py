import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd  # Import pandas with the alias 'pd'
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io  # For saving the plot as a buffer

# Function to calculate FDCI and DCI for each phase
def calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirements, cpis, years):
    fdci_values_no_inflation = []
    fdci_values_with_inflation = []
    dci_values = []
    steel_from_previous = steel_requirements[0]  # Initial steel quantity for Phase 1
    
    for i in range(num_phases):
        # User-defined steel price, reuse factor, CPI, and year for each phase
        cost = steel_prices[i]
        reuse_factor = reuse_factors[i]
        steel_required = steel_requirements[i]
        current_cpi = cpis[i]
        current_year = years[i]
        
        # Calculate steel reuse and procurement from market for each phase
        reused_steel = steel_from_previous * reuse_factor / 100
        procured_steel = steel_required - reused_steel
        
        # FDCI Calculation without inflation
        fdci_no_inflation = reused_steel / (reused_steel + procured_steel * cost)
        fdci_values_no_inflation.append(fdci_no_inflation)
        
        # FDCI Calculation with inflation adjustment
        past_cpi = cpis[0]  # Use the CPI of the first phase (base year)
        adjusted_cost = cost * (current_cpi / past_cpi)
        fdci_with_inflation = reused_steel / (reused_steel + procured_steel * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        # DCI Calculation
        dci = reused_steel / (reused_steel + procured_steel * cost)
        dci_values.append(dci)
        
        # Update mass for the next phase (steel used from previous phase)
        steel_from_previous = reused_steel

    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values

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

# Function to save the plot to a BytesIO buffer
def save_plot_to_buffer(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

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

# Streamlit UI for inputs
def app():
    st.title("FDCI and DCI Calculator")

    num_phases = st.number_input("Enter number of phases", min_value=1, max_value=20, value=3)
    
    # New field to ask the user for the initial steel quantity (tons) for Phase 1
    steel_requirement = []
    steel_requirement.append(st.number_input("Enter initial quantity of steel for Phase 1 (tons)", min_value=1, value=1000))

    steel_prices = []
    reuse_factors = []
    years = []
    cpis = []

    # Gather steel requirements for each phase, starting with Phase 1
    for i in range(1, num_phases):
        steel_requirement.append(st.number_input(f"Phase {i+1} - Steel Requirement (tons)", min_value=1, value=1000))

    for i in range(num_phases):
        steel_prices.append(st.number_input(f"Phase {i+1} - Steel Price (USD per ton)", min_value=0.0, value=500.0))
        reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))
        years.append(st.number_input(f"Phase {i+1} - Year", min_value=1, value=2022))  # No lower bound for the year
        cpis.append(st.number_input(f"Phase {i+1} - CPI", min_value=0.0, value=100.0))

    # Display formulas before showing the results
    st.markdown("""
    ### Formulas Used:
    
    **FDCI (No Inflation Adjustment)**:
    $$ 
    \text{FDCI (No Inflation)} = \frac{{\text{Reused Steel}}}{{\text{Reused Steel} + \text{Procured Steel} \times \text{Cost}}}
    $$
    
    **FDCI (With Inflation Adjustment)**:
    $$ 
    \text{FDCI (With Inflation)} = \frac{{\text{Reused Steel}}}{{\text{Reused Steel} + \text{Procured Steel} \times \text{Adjusted Cost}}}
    $$ 
    Where:
    $$ 
    \text{Adjusted Cost} = \text{Cost} \times \frac{{\text{Current CPI}}}{{\text{Base CPI}}}
    $$

    **DCI**:
    $$ 
    \text{DCI} = \frac{{\text{Reused Steel}}}{{\text{Reused Steel} + \text{Procured Steel} \times \text{Cost}}}
    $$
    """)

    # Start the calculation and display results
    if st.button("Start Calculation"):
        fdci_values_no_inflation, fdci_values_with_inflation, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years)
        
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
