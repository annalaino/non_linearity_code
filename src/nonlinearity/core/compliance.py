"""
Compliance calculation functions.

Extracts BOD and COD limit calculations from the original notebook.
"""

import pandas as pd
import numpy as np

from ..config import ComplianceLimits


def calculate_bod_limits(
    df: pd.DataFrame,
    limits: ComplianceLimits
) -> pd.DataFrame:
    """
    Calculate BOD compliance limits.
    
    Args:
        df: DataFrame with 'bod1' (influent) and 'bod31' (effluent) columns.
        limits: Compliance limits configuration.
    
    Returns:
        DataFrame with added BOD limit columns.
    """
    result = df.copy()
    
    # BOD limit calculations (upper and lower thresholds)
    result['BODut'] = abs(
        (limits.bod_upper - df["bod31"].min()) / 
        (df["bod1"].max() - df["bod31"].min())
    )
    result['BODlt'] = abs(
        (limits.bod_lower - df["bod31"].min()) / 
        (df["bod1"].max() - df["bod31"].min())
    )
    
    return result


def calculate_cod_limits(
    df: pd.DataFrame,
    limits: ComplianceLimits
) -> pd.DataFrame:
    """
    Calculate COD compliance limits.
    
    Args:
        df: DataFrame with 'cod1' (influent) and 'cod31' (effluent) columns.
        limits: Compliance limits configuration.
    
    Returns:
        DataFrame with added COD limit columns.
    """
    result = df.copy()
    
    # COD limit calculations (upper and lower thresholds)
    result['CODut'] = abs(
        (limits.cod_upper - df["cod31"].min()) / 
        (df["cod1"].max() - df["cod31"].min())
    )
    result['CODlt'] = abs(
        (limits.cod_lower - df["cod31"].min()) / 
        (df["cod1"].max() - df["cod31"].min())
    )
    
    return result


def calculate_all_limits(
    df: pd.DataFrame,
    limits: ComplianceLimits = None
) -> pd.DataFrame:
    """
    Calculate both BOD and COD compliance limits.
    
    Args:
        df: DataFrame with required columns.
        limits: Compliance limits. If None, uses defaults.
    
    Returns:
        DataFrame with all limit columns added.
    """
    if limits is None:
        limits = ComplianceLimits()
    
    result = calculate_bod_limits(df, limits)
    result = calculate_cod_limits(result, limits)
    
    return result


def calculate_flag_conditions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate boolean flag conditions for compliance.
    
    Args:
        df: DataFrame with BODut, BODlt, CODut, CODlt columns.
    
    Returns:
        DataFrame with added flag columns.
    """
    result = df.copy()
    
    # Flag conditions based on limit thresholds
    result["flag_BODlt"] = result['BODlt-BODeffl'] >= 0
    result["flag_BODut"] = result['BODut-BODeffl'] >= 0
    result["flag_CODlt"] = result['CODlt-CODeffl'] >= 0
    result["flag_reduction_bod"] = result["bodp"] >= 0
    result["flag_reduction_cod"] = result["codp"] >= 0
    result["flag_CODut"] = result['CODut-CODeffl'] >= 0
    
    return result


def calculate_failure_conditions(
    df: pd.DataFrame
) -> dict:
    """
    Calculate failure conditions for BOD and COD.
    
    Args:
        df: DataFrame with flag columns.
    
    Returns:
        Dictionary with boolean Series for each failure condition.
    """
    # BOD FAILURE conditions
    bod_lut_exc = (
        (df['bod_psi_2'] < 0) & 
        (df["flag_BODlt"] == False) & 
        (df["flag_reduction_bod"] == False) & 
        (df["flag_BODut"] == True)
    )
    bod_max_lim = (
        (df['bod_psi_3'] < 0) & 
        (df["flag_BODlt"] == False) & 
        (df["flag_BODut"] == False) & 
        (df["flag_reduction_bod"] == False)
    )
    
    # COD FAILURE conditions
    cod_lut_exc = (
        (df['cod_psi_2'] < 0) & 
        (df["flag_CODlt"] == False) & 
        (df["flag_reduction_cod"] == False) & 
        (df["flag_CODut"] == True)
    )
    cod_max_lim = (
        (df['cod_psi_3'] < 0) & 
        (df["flag_CODlt"] == False) & 
        (df["flag_CODut"] == False) & 
        (df["flag_reduction_cod"] == False)
    )
    
    return {
        "bod_lut_exc": bod_lut_exc,
        "bod_max_lim": bod_max_lim,
        "cod_lut_exc": cod_lut_exc,
        "cod_max_lim": cod_max_lim,
    }
