"""
linearisation functions.

Extracts linearisation calculations from the original notebook.
"""

import pandas as pd
import numpy as np


def linearise_bod(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply linearisation to BOD influent and effluent data.
    
    Normalises the data using min-max normalisation based on
    the influent maximum and effluent minimum values.
    
    Args:
        df: DataFrame with 'bod1' (influent) and 'bod31' (effluent) columns.
    
    Returns:
        DataFrame with added LIN_BODi and LIN_BODe columns.
    """
    result = df.copy()
    
    # linearisation of BOD influent and effluent
    result["LIN_BODe"] = abs(
        (df["bod31"] - df["bod31"].min()) / 
        (df["bod1"].max() - df["bod31"].min())
    )
    result["LIN_BODi"] = abs(
        (df["bod1"] - df["bod31"].min()) / 
        (df["bod1"].max() - df["bod31"].min())
    )
    
    return result


def linearise_cod(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply linearisation to COD influent and effluent data.
    
    Normalises the data using min-max normalisation based on
    the influent maximum and effluent minimum values.
    
    Args:
        df: DataFrame with 'cod1' (influent) and 'cod31' (effluent) columns.
    
    Returns:
        DataFrame with added LIN_CODi and LIN_CODe columns.
    """
    result = df.copy()
    
    # linearisation of COD influent and effluent
    result["LIN_CODe"] = abs(
        (df["cod31"] - df["cod31"].min()) / 
        (df["cod1"].max() - df["cod31"].min())
    )
    result["LIN_CODi"] = abs(
        (df["cod1"] - df["cod31"].min()) / 
        (df["cod1"].max() - df["cod31"].min())
    )
    
    return result


def apply_linearisation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply linearisation to both BOD and COD data.
    
    Args:
        df: DataFrame with required columns.
    
    Returns:
        DataFrame with all linearisation columns.
    """
    result = linearise_bod(df)
    result = linearise_cod(result)
    
    return result


def calculate_deviation_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate deviation columns from limits and linearisad values.
    
    Args:
        df: DataFrame with limit and linearisation columns.
    
    Returns:
        DataFrame with added deviation columns.
    """
    result = df.copy()
    
    # Calculate differences from limits
    result['BODut-BODeffl'] = (result["BODut"] - result["LIN_BODe"])
    result['CODut-CODeffl'] = (result["CODut"] - result["LIN_CODe"])
    result['BODlt-BODeffl'] = (result["BODlt"] - result["LIN_BODe"])
    result['CODlt-CODeffl'] = (result["CODlt"] - result["LIN_CODe"])
    
    return result


def calculate_reduction_columns(
    df: pd.DataFrame,
    bod_pc: float = 0.7,
    cod_pc: float = 0.75
) -> pd.DataFrame:
    """
    Calculate reduction (psi) percentage columns.
    
    Args:
        df: DataFrame with linearisad columns.
        bod_pc: BOD percentage factor.
        cod_pc: COD percentage factor.
    
    Returns:
        DataFrame with added reduction columns.
    """
    result = df.copy()
    
    # Calculate reduction percentage
    result["bodp"] = -(bod_pc * result["LIN_BODi"]) + result["LIN_BODi"] - result["LIN_BODe"]
    result["codp"] = -(cod_pc * result["LIN_CODi"]) + result["LIN_CODi"] - result["LIN_CODe"]
    
    return result
