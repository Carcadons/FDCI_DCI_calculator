import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_graphs(phases, fdci_values_no_inflation, fdci_values_with_inflation, dci_values):
    """
    Plot the FDCI and DCI graphs for the given phases.
    Arguments:
    - phases: List of phase years.
    - fdci_values_no_inflation: List of FDCI values without inflation adjustment.
    - fdci_values_with_inflation: List of FDCI values with inflation adjustment.
    - dci_values: List of DCI values.
    
    Returns:
    - fig1: Figure object for FDCI graph.
    - fig2: Figure object for DCI graph.
    - fig3: Figure object for FDCI and DCI comparison graph.
    """
    # Plot FDCI with both adjusted and non-adjusted for inflation
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(phases, fdci_values_no_inflation, label="FDCI (No Infl. Adj.)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax1.plot(phases, fdci_values_with_inflation, label="FDCI (With Infl. Adj.)", marker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    ax1.set_xlabel('Phase', fontsize=12)
    ax1.set_ylabel('FDCI', fontsize=12)
    ax1.set_title('FDCI Comparison: Inflation Adjusted vs. Non-Adjusted', fontsize=14)
    ax1.grid(True)
    ax1.legend(title="LEGEND", fontsize=10)
    
    # Plot DCI
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(phases, dci_values, label="DCI", marker='o', linestyle='--', color='red', linewidth=2, markersize=8)
    ax2.set_xlabel('Phase', fontsize=12)
    ax2.set_ylabel('DCI', fontsize=12)
    ax2.set_title('DCI Across Phases', fontsize=14)
    ax2.grid(True)
    ax2.legend(title="LEGEND", fontsize=10)

    # Plot FDCI and DCI together
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(phases, fdci_values_no_inflation, label="FDCI (No Infl. Adj.)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax3.plot(phases, fdci_values_with_inflation, label="FDCI (With Infl. Adj.)", marker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    ax3.plot(phases, dci_values, label="DCI", marker='o', linestyle='--', color='red', linewidth=2, markersize=8)
    ax3.set_xlabel('Phase', fontsize=12)
    ax3.set_ylabel('Value', fontsize=12)
    ax3.set_title('FDCI and DCI Comparison', fontsize=14)
    ax3.grid(True)
    ax3.legend(title="LEGEND", fontsize=10)

    return fig1, fig2, fig3

def plot_comparison_graph(phases, fdci_values_no_inflation, fdci_values_with_inflation, dci_values):
    # Invert DCI for better comparison
    inverted_dci_values = [1 - dci for dci in dci_values]

    # Plot FDCI and Inverted DCI
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot FDCI values (No Inflation and With Inflation)
    ax1.plot(phases, fdci_values_no_inflation, label="FDCI (No Infl. Adj.)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax1.plot(phases, fdci_values_with_inflation, label="FDCI (With Infl.Adj.)", marker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    ax1.set_xlabel('Phase')
    ax1.set_ylabel('FDCI', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for the inverted DCI
    ax2 = ax1.twinx()
    ax2.plot(phases, inverted_dci_values, label="Inverted DCI", marker='o', linestyle='--', color='red', linewidth=2, markersize=8)
    ax2.set_ylabel('Inverted DCI', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add title and legend
    plt.title('Comparison of FDCI and Inverted DCI')
    fig.tight_layout()  # Adjust layout to prevent overlap

    # Show legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='bottom left')
    ax1.legend(title="LEGEND", fontsize=10)
    ax2.legend(title="LEGEND", fontsize=10)

    # Display the plot in Streamlit
    return fig

def plot_material_cost_comparison(years, inflation_adjusted_costs, non_inflation_adjusted_costs, material_type):
    """
    Plot the comparison of material costs (with and without inflation adjustment).
    Arguments:
    - years: List of phase years.
    - inflation_adjusted_costs: List of material costs adjusted for inflation.
    - non_inflation_adjusted_costs: List of material costs without inflation adjustment.
    - material_type: String indicating the material type (steel, wood, concrete).
    
    Returns:
    - fig: Figure object for the material cost comparison graph.
    """
    fig4, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(years, non_inflation_adjusted_costs, label="Material Cost (No Infl. Adj.)", marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    ax.plot(years, inflation_adjusted_costs, label="Material Cost (With Infl. Adj.)", mmarker='o', linestyle='-', color='green', linewidth=2, markersize=8)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Material Cost (USD)', fontsize=12)
    ax.set_title(f'{material_type.capitalize()} Material Cost (Wiht and Without Infl. Adj. Comparison)', fontsize=14)
    ax.grid(True)
    ax.legend(title="LEGEND", fontsize=10)

    return fig4
