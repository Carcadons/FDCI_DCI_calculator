import numpy as np
import matplotlib.pyplot as plt
import streamlit as st  # Ensure Streamlit is imported
import pandas as pd  # Import pandas with the alias 'pd'
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io  # For saving the plot as a buffer

cpi_database = {
    1900: 8.4, 1901: 8.5, 1902: 8.3, 1903: 8.5, 1904: 8.6, 1905: 8.7,
    1906: 8.9, 1907: 9.1, 1908: 9.2, 1909: 9.4, 1910: 9.6, 1911: 9.8,
    1912: 10.0, 1913: 10.3, 1914: 10.6, 1915: 11.0, 1916: 11.5, 1917: 12.0,
    1918: 13.0, 1919: 14.0, 1920: 15.0, 1921: 14.8, 1922: 14.9, 1923: 15.0,
    1924: 15.2, 1925: 15.5, 1926: 15.7, 1927: 15.8, 1928: 16.0, 1929: 16.3,
    1930: 15.9, 1931: 15.6, 1932: 15.3, 1933: 15.1, 1934: 15.2, 1935: 15.3,
    1936: 15.5, 1937: 15.6, 1938: 15.8, 1939: 16.0, 1940: 16.3, 1941: 16.5,
    1942: 17.0, 1943: 17.5, 1944: 17.8, 1945: 18.0, 1946: 18.5, 1947: 19.0,
    1948: 19.5, 1949: 19.9, 1950: 20.0, 1951: 20.5, 1952: 20.9, 1953: 21.2,
    1954: 21.5, 1955: 21.8, 1956: 22.0, 1957: 22.5, 1958: 22.7, 1959: 23.0,
    1960: 23.5, 1961: 24.0, 1962: 24.4, 1963: 24.9, 1964: 25.2, 1965: 25.5,
    1966: 25.9, 1967: 26.3, 1968: 26.7, 1969: 27.0, 1970: 27.5, 1971: 28.0,
    1972: 28.5, 1973: 29.0, 1974: 29.5, 1975: 30.0, 1976: 30.5, 1977: 31.0,
    1978: 31.5, 1979: 32.0, 1980: 33.5, 1981: 34.0, 1982: 34.5, 1983: 35.0,
    1984: 35.5, 1985: 36.0, 1986: 36.5, 1987: 37.0, 1988: 37.5, 1989: 38.0,
    1990: 38.5, 1991: 39.0, 1992: 39.5, 1993: 40.0, 1994: 40.5, 1995: 41.0,
    1996: 41.5, 1997: 42.0, 1998: 42.5, 1999: 43.0, 2000: 43.5, 2001: 44.0,
    2002: 44.5, 2003: 45.0, 2004: 45.5, 2005: 46.0, 2006: 46.5, 2007: 47.0,
    2008: 47.5, 2009: 48.0, 2010: 48.5, 2011: 49.0, 2012: 49.5, 2013: 50.0,
    2014: 50.5, 2015: 51.0, 2016: 51.5, 2017: 52.0, 2018: 52.5, 2019: 53.0,
    2020: 53.5, 2021: 54.0, 2022: 54.5, 2023: 55.0, 2024: 55.5, 2025: 56.0
}

# Function to calculate FDCI and DCI for each phase
def calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirements, cpis, years):
    fdci_values_no_inflation = []
    fdci_values_with_inflation = []
    dci_values = []
    steel_from_previous = steel_requirements[0]  # Initial steel quantity for Phase 1
    
    for i in range(num_phases):
        cost = steel_prices[i]
        reuse_factor = reuse_factors[i]
        steel_required = steel_requirements[i]
        current_cpi = cpis[i]
        current_year = years[i]
        
        reused_steel = steel_from_previous * reuse_factor / 100
        procured_steel = steel_required - reused_steel
        
        fdci_no_inflation = reused_steel / (reused_steel + procured_steel * cost)
        fdci_values_no_inflation.append(fdci_no_inflation)
        
        past_cpi = cpis[0]
        adjusted_cost = cost * (current_cpi / past_cpi)
        fdci_with_inflation = reused_steel / (reused_steel + procured_steel * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        dci = reused_steel / (reused_steel + procured_steel * cost)
        dci_values.append(dci)
        
        steel_from_previous = reused_steel

    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values

# Function to save the plot to a BytesIO buffer
def save_plot_to_buffer(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Streamlit UI for inputs
def app():
    st.title("FDCI and DCI Calculator")

    num_phases = st.number_input("Enter number of phases", min_value=1, max_value=20, value=3)
    
    # Ask the user if they want to use the default CPI database or manually input CPIs
    use_cpi_database = st.checkbox("Use default CPI database (1900-2025)")
    
    # If using CPI database, fill in the CPIs automatically; otherwise, allow manual input
    cpis = []
    for i in range(num_phases):
        if use_cpi_database:
            # Allow the user to select a year for each phase and use the CPI from the database
            year = st.number_input(f"Select Year for Phase {i+1} (1900-2025)", min_value=1900, max_value=2025, value=2022)
            cpis.append(cpi_database.get(year, 100))  # Default to 100 if CPI is not available for the selected year
        else:
            # Manually input CPI
            cpis.append(st.number_input(f"Enter CPI for Phase {i+1}", min_value=0.0, value=100.0))

    # Gather other inputs
    steel_requirement = [st.number_input("Enter initial quantity of steel for Phase 1 (tons)", min_value=1, value=1000)]
    steel_prices = [st.number_input(f"Phase 1 - Steel Price (USD per ton)", min_value=0.0, value=500.0)]
    reuse_factors = [st.number_input(f"Phase 1 - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0)]
    years = [2022]  # Default to the current year

    # Gather the rest of the data
    for i in range(1, num_phases):
        steel_requirement.append(st.number_input(f"Phase {i+1} - Steel Requirement (tons)", min_value=1, value=1000))
        steel_prices.append(st.number_input(f"Phase {i+1} - Steel Price (USD per ton)", min_value=0.0, value=500.0))
        reuse_factors.append(st.number_input(f"Phase {i+1} - Reuse Factor (%)", min_value=0.0, max_value=100.0, value=75.0))
        years.append(st.number_input(f"Phase {i+1} - Year", min_value=1900, max_value=2025, value=2022))

    # Start the calculation and display results
    if st.button("Start Calculation"):
        fdci_values_no_inflation, fdci_values_with_inflation, dci_values = calculate_indices(num_phases, steel_prices, reuse_factors, steel_requirement, cpis, years)
        
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
