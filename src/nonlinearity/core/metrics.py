"""
Metrics calculation functions.

Extracts PSI (Performance Sustainability Index) and metric calculations
from the original notebook.
"""

import pandas as pd
import numpy as np

from ..config import ComplianceLimits, REQUIRED_COLUMNS
from ..data.validators import validate_dataframe, check_required_columns
from .compliance import (
    calculate_all_limits,
    calculate_flag_conditions,
)
from .linearisation import (
    apply_linearisation,
    calculate_deviation_columns,
    calculate_reduction_columns,
)


def calculate_psi_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate PSI (Performance Sustainability Index) values for BOD and COD.
    
    Args:
        df: DataFrame with deviation columns:
            - BODlt-BODeffl, BODut-BODeffl, bodp
            - CODlt-CODeffl, CODut-CODeffl, codp
    
    Returns:
        DataFrame with added PSI columns.
    """
    result = df.copy()
    
    # BOD PSI calculations
    result["bod_psi_1_min"] = result[['BODlt-BODeffl', 'bodp']].min(axis=1)
    result["bod_psi_1"] = result[['BODlt-BODeffl', 'bod_psi_1_min']].max(axis=1)
    result["bod_psi_2"] = result[['BODlt-BODeffl', 'bodp', "BODut-BODeffl"]].min(axis=1)
    result["bod_psi_3"] = result[["BODut-BODeffl", "bodp"]].min(axis=1)
    
    # COD PSI calculations
    result["cod_psi_1_min"] = result[['CODlt-CODeffl', 'codp']].min(axis=1)
    result["cod_psi_1"] = result[['CODlt-CODeffl', 'cod_psi_1_min']].max(axis=1)
    result["cod_psi_2"] = result[['CODlt-CODeffl', 'codp', "CODut-CODeffl"]].min(axis=1)
    result["cod_psi_3"] = result[["CODut-CODeffl", "codp"]].min(axis=1)
    
    return result


def calculate_metric_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate metric values (combined PSI metrics).
    
    Args:
        df: DataFrame with PSI columns.
    
    Returns:
        DataFrame with added metric columns.
    """
    result = df.copy()
    
    # metric LUT (Look-Up Table)
    result["metric_lut"] = result[["bod_psi_2", "cod_psi_2"]].min(axis=1)
    
    # metric MAX
    result["metric_max"] = result[["bod_psi_3", "cod_psi_3"]].min(axis=1)
    
    return result


def determine_failure_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Determine failure type and source based on conditions.
    
    Args:
        df: DataFrame with metric and flag columns.
    
    Returns:
        DataFrame with added fail_type and fail_source columns.
    """
    result = df.copy()
    
    # Define failure conditions
    bod_lut_exc = (
        (result['bod_psi_2'] < 0) & 
        (result["flag_BODlt"] == False) & 
        (result["flag_reduction_bod"] == False) & 
        (result["flag_BODut"] == True)
    )
    bod_max_lim = (
        (result['bod_psi_3'] < 0) & 
        (result["flag_BODlt"] == False) & 
        (result["flag_BODut"] == False) & 
        (result["flag_reduction_bod"] == False)
    )
    cod_lut_exc = (
        (result['cod_psi_2'] < 0) & 
        (result["flag_CODlt"] == False) & 
        (result["flag_reduction_cod"] == False) & 
        (result["flag_CODut"] == True)
    )
    cod_max_lim = (
        (result['cod_psi_3'] < 0) & 
        (result["flag_CODlt"] == False) & 
        (result["flag_CODut"] == False) & 
        (result["flag_reduction_cod"] == False)
    )
    
    # Combined conditions
    condition_2 = (bod_lut_exc | cod_lut_exc)
    condition_3 = (bod_max_lim | cod_max_lim)
    
    # Metric selection logic
    cond_lut = condition_2 & ~condition_3
    cond_max = condition_2 & condition_3
    
    choices = [result["metric_lut"], result["metric_max"]]
    default_val = result[['bod_psi_1', 'cod_psi_1']].max(axis=1)
    
    result["metric"] = np.select([cond_lut, cond_max], choices, default=default_val)
    
    # Assign fail_type
    fail_type_conditions = [
        bod_lut_exc, bod_max_lim,  # BOD conditions
        cod_lut_exc, cod_max_lim   # COD conditions
    ]
    fail_type_values = [
        "LUT exceedance", "Max Limit Failure",  # BOD fail types
        "LUT exceedance", "Max Limit Failure"   # COD fail types
    ]
    result["fail_type"] = np.select(
        fail_type_conditions, 
        fail_type_values, 
        default="Compliant"
    )
    
    # Assign fail_source
    result["fail_source"] = np.select(
        [bod_lut_exc | bod_max_lim, cod_lut_exc | cod_max_lim],
        ["BOD", "COD"],
        default="None"
    )
    
    # Store intermediate flags
    result["bod_lut_exc"] = bod_lut_exc
    result["bod_max_lim"] = bod_max_lim
    result["cod_lut_exc"] = cod_lut_exc
    result["cod_max_lim"] = cod_max_lim
    
    # Additional comparison flags
    result['c_BOD_2'] = result["bod_psi_2"] < result["cod_psi_2"]
    result['c_BOD_3'] = result["bod_psi_3"] < result["cod_psi_3"]
    
    return result


def process_dataframe(
    df: pd.DataFrame,
    limits: ComplianceLimits = None
) -> pd.DataFrame:
    """
    Process a complete DataFrame through all compliance calculations.
    
    This is the main entry point for processing scenario data.
    
    Args:
        df: Raw DataFrame with required columns.
        limits: Compliance limits. If None, uses defaults.
    
    Returns:
        Fully processed DataFrame with all calculations.
    
    Raises:
        DataValidationError: If required columns are missing.
    """
    if limits is None:
        limits = ComplianceLimits()
    
    # Validate input data
    validate_dataframe(df, REQUIRED_COLUMNS, allow_empty=False)
    
    # Step 1: Calculate limits
    result = calculate_all_limits(df, limits)
    
    # Step 2: Apply linearisation
    result = apply_linearisation(result)
    
    # Step 3: Calculate deviation columns
    result = calculate_deviation_columns(result)
    
    # Step 4: Calculate reduction columns
    result = calculate_reduction_columns(
        result, 
        limits.bod_pc, 
        limits.cod_pc
    )
    
    # Step 5: Calculate flag conditions
    result = calculate_flag_conditions(result)
    
    # Step 6: Calculate PSI values
    result = calculate_psi_values(result)
    
    # Step 7: Calculate metric values
    result = calculate_metric_values(result)
    
    # Step 8: Determine failure types
    result = determine_failure_type(result)
    
    return result
