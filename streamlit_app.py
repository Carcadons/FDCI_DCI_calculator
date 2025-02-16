import streamlit as st
import pandas as pd  # Make sure to import pandas
from cpi_utils import load_cpi_data
from material_utils import load_material_prices
from calculations import calculate_indices
from plot_utils import plot_graphs, save_plot_to_buffer, display_table

def app():
    st.title("FDCI and DCI Calculator")

    # Load CPI data from the external JSON file
    cpi_database = load_cpi_data()

    # Allow user to select the material (steel, wood, or concrete)
    material_type = st.selectbox("Select Material for Calculation", ["steel", "wood", "concrete"])

    # Load material prices from the selected material type
    material_prices_data = load_material_prices(material_type)

    # Ask the user to define the number of phases
    num_phases = st.number_input("Enter number of phases", min_value=1, max_value=25, value=3)

    # Ask the user to input phase year
    years_input = st.text_input("Enter years for all phases (comma-separated)", value="1900,1950,2025")
    # Split the input by commas to create a list of years
    years = [int(year.strip()) for year in years_input.split(',')]
    # Validate that the number of years matches the number of phases
    if len(years) != num_phases:
        st.error(f"Please enter exactly {num_phases} years for the phases.")
    
    # Ask the user if they want to use the default CPI database or manually input CPIs
    use_cpi_database = st.checkbox("Use default CPI database (1900-2025)")
    
    # Input for CPI values
    cpis = []
    for i in range(num_phases):
        if use_cpi_database:
            year = st.number_input(f"Select Year for Phase {i+1} (1900-2025)", min_value=1900, max_value=2025, value=2022)
            cpis.append(cpi_database.get(str(year), 100))  # Default to 100 if CPI is not available for the selected year
        else:
            cpis.append(st.number_input(f"Enter CPI for Phase {i+1}", min_value=0.0, value=100.0))

    # Ask the user if they want to use the material price database or manually input values
    use_material_price_database = st.checkbox(f"Use default {material_type.capitalize()} Price database (1900-2025)")

    material_prices = []
    for i in range(num_phases):
        if use_material_price_database:
            year = st.number_input(f"Select Year for Phase {i+1} {material_type.capitalize()} Price (1900-2025)", min_value=1900, max_value=2025, value=2022)
            price = material_prices_data.get(str(year), 500)
            material_prices.append(price)
        else:
            material_prices.append(st.number_input(f"Enter {material_type.capitalize()} Price for Phase {i+1} (USD per unit)", min_value=0.0, value=500.0))

    # Display a recap table for CPI and Material Prices
    recap_data = {
        "Phase": [f"Phase {i+1}" for i in range(num_phases)],
        "Year": years,
        "CPI": cpis,
        f"{material_type.capitalize()} Price (USD)": material_prices
    }
    recap_df = pd.DataFrame(recap_data)
    st.write("### Recap Table: CPI and Material Prices for Each Phase")
    st.write(recap_df)

    # Gather other inputs for the material requirements and reuse factors
    material_requirement = [st.number_input(f"Enter initial quantity of {material_type} for Phase 1 (tons)", min_value=1, value=1000)]
    reuse_factors = [st.number_input(f"Phase 1 - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0)]

    for i in range(1, num_phases):
        material_requirement.append(st.number_input(f"Phase {i+1} - Material Requirement (tons)", min_value=1, value=1000))
        reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))

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
