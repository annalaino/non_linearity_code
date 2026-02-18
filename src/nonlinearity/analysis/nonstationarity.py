"""
Non-stationarity analysis functions.

Extracts non-stationarity scoring from the original notebook.
"""

from typing import List, Optional

import pandas as pd
import numpy as np


def non_stationarity_score(
    series: pd.Series,
    window: int = 30
) -> float:
    """
    Calculate a numeric score indicating non-stationarity.
    
    Higher score indicates more non-stationarity.
    
    The score is calculated as the mean absolute deviation of rolling 
    variance normalised by overall variance.
    
    Args:
        series: Time series data.
        window: Rolling window size for variance calculation.
    
    Returns:
        Non-stationarity score (float).
    """
    if len(series) < window:
        return np.nan
    
    # Remove NaN values
    clean_series = series.dropna()
    
    if len(clean_series) < window:
        return np.nan
    
    rolling_var = clean_series.rolling(window=window).var()
    overall_var = clean_series.var()
    
    if overall_var == 0:
        return 0.0
    
    # Calculate normalised score
    score = (rolling_var - overall_var).abs().mean() / overall_var
    
    return float(score)


def compute_nonstationarity_table(
    results: dict,
    columns: List[str] = None
) -> pd.DataFrame:
    """
    Compute non-stationarity scores for all scenarios.
    
    Args:
        results: Dictionary mapping scenario names to DataFrames.
        columns: List of columns to analyse. Defaults to linearised columns.
    
    Returns:
        DataFrame with non-stationarity scores.
    """
    if columns is None:
        columns = ["LIN_BODi", "LIN_BODe", "LIN_CODi", "LIN_CODe"]
    
    rows = []
    
    for scenario_name, df in results.items():
        if df.empty:
            continue
        
        row = {"Dataset": scenario_name}
        
        for col in columns:
            if col in df.columns:
                row[col] = non_stationarity_score(df[col])
        
        rows.append(row)
    
    return pd.DataFrame(rows)


def compute_rolling_statistics(
    series: pd.Series,
    window: int = 30
) -> pd.DataFrame:
    """
    Compute rolling statistics for a time series.
    
    Args:
        series: Time series data.
        window: Rolling window size.
    
    Returns:
        DataFrame with rolling mean, std, and variance.
    """
    return pd.DataFrame({
        'rolling_mean': series.rolling(window=window).mean(),
        'rolling_std': series.rolling(window=window).std(),
        'rolling_var': series.rolling(window=window).var(),
        'rolling_median': series.rolling(window=window).median(),
    })
