import streamlit as st
import pandas as pd

def calculate_indices(num_phases, material_prices, reuse_factors, material_requirements, cpis, years):
    fdci_values_no_inflation = []
    fdci_values_with_inflation = []
    dci_values = []
    
    # Initial material quantity for Phase 1
    material_from_previous = material_requirements[0]
    
    for i in range(num_phases):
        # Get the current phase data
        cost = material_prices[i]  # Material cost for the phase
        reuse_factor = reuse_factors[i]  # Reuse factor for the phase
        material_required = material_requirements[i]  # Material required for the phase
        past_cpi = cpis[i]  # CPI for the current phase (the past CPI for that phase)
        today_cpi = 300.0  # Assume today's CPI is 300
        current_year = years[i]  # Year for the current phase
        
        # Reused material based on the reuse factor
        reused_material = material_from_previous * reuse_factor / 100
        
        # Procured material (material required minus reused material)
        procured_material = material_required - reused_material
        
        # FDCI without inflation (reused material / (procured material * cost))
        fdci_no_inflation = reused_material / (procured_material * cost)
        fdci_values_no_inflation.append(fdci_no_inflation)
        
        # Inflation-adjusted cost using CPI values
        adjusted_cost = cost * (today_cpi / past_cpi)  # Adjust cost based on today's CPI relative to past CPI
        
        # FDCI with inflation adjustment
        fdci_with_inflation = reused_material / (procured_material * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        # DCI calculation (reused material / (material required * cost))
        dci = reused_material / (material_required * cost)
        dci_values.append(dci)
        
        # Update the material for the next phase to the reused material from this phase
        material_from_previous = reused_material
    
    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values

def calculate_material_costs(material_prices, cpis, num_phases):
    inflation_adjusted_costs = []
    non_inflation_adjusted_costs = []

    for i in range(num_phases):
        # Calculate inflation-adjusted cost using the formula:
        inflation_adjusted_cost = material_prices[i] * (today_cpi / past_cpi)  # Adjust for CPI
        inflation_adjusted_costs.append(inflation_adjusted_cost)
        non_inflation_adjusted_costs.append(material_prices[i])

    return inflation_adjusted_costs, non_inflation_adjusted_costs
