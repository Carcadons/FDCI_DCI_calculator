import streamlit as st
import pandas as pd  # Make sure to import pandas
from cpi_utils import load_cpi_data
from material_utils import load_material_prices
from calculations import calculate_indices, calculate_material_costs
from plot_utils import plot_graphs, plot_material_cost_comparison, save_plot_to_buffer

# Function to display the results table in Streamlit
def display_table(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values):
    """
    Display the results of FDCI and DCI calculations in a table format in Streamlit.
    Arguments:
    - years: List of phase years.
    - fdci_values_no_inflation: List of FDCI values without inflation adjustment.
    - fdci_values_with_inflation: List of FDCI values with inflation adjustment.
    - dci_values: List of DCI values.
    """
    results_data = {
        "Phase Year": years,
        "FDCI (No Infl. Adj.)": fdci_values_no_inflation,
        "FDCI (With Infl. Adj.)": fdci_values_with_inflation,
        "DCI": dci_values
    }
    
    results_df = pd.DataFrame(results_data)
    st.write("### Results Table: FDCI and DCI")
    st.dataframe(results_df)  # Use st.dataframe instead of st.write

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
    use_cpi_database = st.checkbox("Use default U.S. CPI database (1900-2025)")
    
    # Ask the user to input phase years all at once
    years_input = st.text_input("Enter years for all phases (comma-separated)", value="2022,2023,2024")

    # Split the input by commas to create a list of years
    years = [int(year.strip()) for year in years_input.split(',')]

    # Validate that the number of years matches the number of phases
    if len(years) != num_phases:
        st.error(f"Please enter exactly {num_phases} years for the phases.")

    # If using CPI database, fetch CPI values for the entered years
    if use_cpi_database:
        cpis = []
        for year in years:
            # Check if the year exists in the CPI database
            cpi_value = cpi_database.get(str(year), None)
            if cpi_value is None:
                st.warning(f"CPI data for {year} is not available. Defaulting to 100.")
                cpis.append(100)  # Default to 100 if CPI data is missing
            else:
                cpis.append(cpi_value)
    else:
        # If the user does not want to use the CPI database, allow manual input
        cpis = []
        for i in range(num_phases):
            cpis.append(st.number_input(f"Enter CPI for Phase {i+1}", min_value=0.0, value=100.0))

    # Ask the user if they want to use the material price database or manually input values
    use_material_price_database = st.checkbox(f"Use default {material_type.capitalize()} Price database (1900-2025)")

    material_prices = []
    for i in range(num_phases):
        if use_material_price_database:
            # Fetch the material price for the selected year from the database
            year = years[i]  # Use the year for the corresponding phase
            price = material_prices_data.get(str(year), 500)  # Default to 500 if year is not found
            material_prices.append(price)
        else:
            material_prices.append(st.number_input(f"Enter {material_type.capitalize()} Price for Phase {i+1} (USD per unit)", min_value=0.0, value=500.0))

    # Display a summary table for CPI and Material Prices
    recap_data = {
        "Phase": [f"Phase {i+1}" for i in range(num_phases)],
        "Year": years,
        "CPI": cpis,
        f"{material_type.capitalize()} Price (USD)": material_prices
    }
    recap_df = pd.DataFrame(recap_data)
    st.write("### Summary Table: CPI and Material Prices for Each Phase")
    st.dataframe(recap_df)  # Use st.dataframe instead of st.write

    # Ask the user if they want to fix the reuse rate for all phases
    fix_reuse_rate = st.checkbox("Fix the Reuse Rate for All Phases")

    if fix_reuse_rate:
        # Input for reuse rate once
        reuse_factor = st.number_input("Enter the Reuse Factor (%) for All Phases", min_value=0.0, max_value=100.0, value=75.0)
        reuse_factors = [reuse_factor] * num_phases  # Apply the same factor for all phases
    else:
        # Allow the user to input different reuse factors for each phase
        reuse_factors = []
        for i in range(num_phases):
            reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))

    # Ask the user if they want to fix the material quantity for all phases
    fix_material_quantity = st.checkbox("Fix the Material Quantity for All Phases")

    if fix_material_quantity:
        # Input for material quantity once
        material_quantity = st.number_input(f"Enter the Material Quantity (tons) for All Phases", min_value=1, value=1000)
        material_requirement = [material_quantity] * num_phases  # Apply the same quantity for all phases
    else:
        # Allow the user to input different material quantities for each phase
        material_requirement = []
        for i in range(num_phases):
            material_requirement.append(st.number_input(f"Phase {i+1} - Material Requirement (tons)", min_value=1, value=1000))

    # Start the calculation and display results
    if st.button("Calculate"):
        # Calculate FDCI, DCI, and material costs
        fdci_values_no_inflation, fdci_values_with_inflation, dci_values = calculate_indices(num_phases, material_prices, reuse_factors, material_requirement, cpis, years)
        
        # Calculate inflation-adjusted and non-inflation-adjusted material costs
        inflation_adjusted_costs, non_inflation_adjusted_costs = calculate_material_costs(material_prices, cpis, num_phases)
        
        # Display results in table
        display_table(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values)
        
        # Plot the graphs
        fig1, fig2, fig3 = plot_graphs(years, fdci_values_no_inflation, fdci_values_with_inflation, dci_values)
        fig4 = plot_material_cost_comparison(years, inflation_adjusted_costs, non_inflation_adjusted_costs, material_type)
        
        # Display the plots in Streamlit
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)
        st.pyplot(fig4)

        # Save plot button (optional)
        if st.button("Save Plot as PNG"):
            buf1 = save_plot_to_buffer(fig1)
            buf2 = save_plot_to_buffer(fig2)
            buf3 = save_plot_to_buffer(fig3)
            buf4 = save_plot_to_buffer(fig4)
            
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

            st.download_button(
                label="Download Material Cost Comparison Plot (PNG)",
                data=buf4,
                file_name="material_cost_comparison.png",
                mime="image/png"
            )

# Run the Streamlit app
if __name__ == "__main__":
    app()

