"""
Data validation functions.

Provides validation for DataFrames and required columns.
"""

from typing import List, Optional

import pandas as pd

from ..config import REQUIRED_COLUMNS


class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


def check_required_columns(
    df: pd.DataFrame,
    required_columns: List[str] = None,
    raise_error: bool = False
) -> List[str]:
    """
    Check for required columns in a DataFrame.
    
    Args:
        df: DataFrame to validate.
        required_columns: List of required column names. 
                         Defaults to REQUIRED_COLUMNS from config.
        raise_error: If True, raises DataValidationError instead of returning.
    
    Returns:
        List of missing column names. Empty if all present.
    """
    if required_columns is None:
        required_columns = REQUIRED_COLUMNS
    
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing and raise_error:
        raise DataValidationError(
            f"Missing required columns: {missing}. "
            f"Found columns: {list(df.columns)}"
        )
    
    return missing


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: List[str] = None,
    allow_empty: bool = False
) -> bool:
    """
    Validate a DataFrame for basic requirements.
    
    Args:
        df: DataFrame to validate.
        required_columns: List of required column names.
        allow_empty: Whether to allow empty DataFrames.
    
    Returns:
        True if valid.
    
    Raises:
        DataValidationError: If validation fails.
    """
    if df is None:
        raise DataValidationError("DataFrame is None")
    
    if not allow_empty and df.empty:
        raise DataValidationError("DataFrame is empty")
    
    missing = check_required_columns(df, required_columns)
    if missing:
        raise DataValidationError(f"Missing required columns: {missing}")
    
    return True


def validate_numeric_columns(
    df: pd.DataFrame,
    columns: List[str],
    allow_na: bool = False
) -> List[str]:
    """
    Check that specified columns contain numeric data.
    
    Args:
        df: DataFrame to validate.
        columns: List of column names to check.
        allow_na: Whether to allow NA/NaN values.
    
    Returns:
        List of columns with non-numeric data. Empty if all valid.
    """
    invalid = []
    
    for col in columns:
        if col not in df.columns:
            continue
        
        # Check if column can be converted to numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            invalid.append(col)
        elif not allow_na and df[col].isna().any():
            # Check for NaN values if not allowed
            pass  # NaN is valid for numeric columns
    
    return invalid


def get_data_quality_report(df: pd.DataFrame) -> dict:
    """
    Generate a data quality report for a DataFrame.
    
    Args:
        df: DataFrame to analyse.
    
    Returns:
        Dictionary with data quality metrics.
    """
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_columns": check_required_columns(df),
        "null_counts": df.isnull().sum().to_dict(),
        "numeric_columns": [
            col for col in df.columns 
            if pd.api.types.is_numeric_dtype(df[col])
        ],
    }
    
    # Check for columns from original notebook that we expect
    expected_cols = ['bod1', 'cod1', 'bod31', 'cod31']
    report["has_expected_columns"] = all(
        col in df.columns for col in expected_cols
    )
    
    return report
