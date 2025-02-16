import streamlit as st
import pandas as pd

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
        
        # Inflation-adjusted cost using CPI values
        past_cpi = cpis[0]  # Assume CPI of the first phase is the base CPI
        adjusted_cost = cost * (current_cpi / past_cpi)
        fdci_with_inflation = reused_material / (reused_material + procured_material * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        dci = reused_material / (material_requirements * cost)
        dci_values.append(dci)

    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values

def calculate_material_costs(material_prices, cpis, num_phases):
    inflation_adjusted_costs = []
    non_inflation_adjusted_costs = []

    for i in range(num_phases):
        # Calculate inflation-adjusted cost using the formula:
        inflation_adjusted_cost = material_prices[i] * (cpis[0] / cpis[i])  # Adjust for CPI
        inflation_adjusted_costs.append(inflation_adjusted_cost)
        non_inflation_adjusted_costs.append(material_prices[i])

    return inflation_adjusted_costs, non_inflation_adjusted_costs
