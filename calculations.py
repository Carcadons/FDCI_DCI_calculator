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
        
        past_cpi = cpis[0]
        adjusted_cost = cost * (current_cpi / past_cpi)
        fdci_with_inflation = reused_material / (reused_material + procured_material * adjusted_cost)
        fdci_values_with_inflation.append(fdci_with_inflation)
        
        dci = reused_material / (reused_material + procured_material * cost)
        dci_values.append(dci)
        
        material_from_previous = reused_material

    return fdci_values_no_inflation, fdci_values_with_inflation, dci_values
