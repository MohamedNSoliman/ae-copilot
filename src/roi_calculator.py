"""
ROI Calculator for Cursor developer productivity.
Deterministic calculations - no LLM required.
"""

from .schemas import ROIInputs, ROIOutputs


def calculate_roi(inputs: ROIInputs) -> ROIOutputs:
    """
    Calculate ROI metrics for Cursor adoption.
    
    Args:
        inputs: ROI input parameters
        
    Returns:
        ROIOutputs with calculated metrics
    """
    # Calculate annual hours saved
    # Formula: team_size * hours_per_week * adoption_rate * weeks_per_year
    annual_hours_saved = (
        inputs.team_size_engineering
        * inputs.hours_saved_per_engineer_per_week
        * inputs.adoption_rate
        * inputs.weeks_per_year
    )
    
    # Calculate annual cost saved
    # Formula: (annual_hours_saved / (weeks_per_year * hours_per_week_per_engineer)) * fully_loaded_cost
    # Assuming 40 hours per week per engineer
    hours_per_week_per_engineer = 40
    annual_hours_per_engineer = inputs.weeks_per_year * hours_per_week_per_engineer
    equivalent_engineers_saved = annual_hours_saved / annual_hours_per_engineer
    annual_cost_saved = equivalent_engineers_saved * inputs.fully_loaded_cost_per_engineer
    
    # Net annual value = savings - cost
    net_annual_value = annual_cost_saved - inputs.cursor_annual_cost
    
    # Payback period in months
    # Formula: (cursor_annual_cost / annual_cost_saved) * 12
    if annual_cost_saved > 0:
        payback_months = (inputs.cursor_annual_cost / annual_cost_saved) * 12
    else:
        payback_months = float('inf')
    
    return ROIOutputs(
        annual_hours_saved=round(annual_hours_saved, 2),
        annual_cost_saved=round(annual_cost_saved, 2),
        net_annual_value=round(net_annual_value, 2),
        payback_months=round(payback_months, 2) if payback_months != float('inf') else float('inf')
    )
