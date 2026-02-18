"""
Statistical analysis functions.

Extracts statistical calculations from the original notebook.
"""

from typing import Dict, List, Optional

import pandas as pd
import numpy as np


def compute_summary_stats(
    df: pd.DataFrame,
    columns: List[str] = None
) -> pd.DataFrame:
    """
    Compute summary statistics for specified columns.
    
    Args:
        df: DataFrame to analyse.
        columns: List of column names. If None, uses default BOD/COD columns.
    
    Returns:
        DataFrame with mean, std, min, max for each column.
    """
    if columns is None:
        columns = ['bod1', 'bod31', 'cod1', 'cod31']
    
    # Filter to existing columns
    columns = [col for col in columns if col in df.columns]
    
    stats = {
        'mean': df[columns].mean(),
        'std': df[columns].std(),
        'min': df[columns].min(),
        'max': df[columns].max(),
    }
    
    return pd.DataFrame(stats, index=columns).T


def compute_cv(
    df: pd.DataFrame,
    columns: List[str] = None
) -> pd.Series:
    """
    Compute Coefficient of Variation (CV = std/mean).
    
    Args:
        df: DataFrame to analyse.
        columns: List of column names. If None, uses default BOD/COD columns.
    
    Returns:
        Series with CV values.
    """
    if columns is None:
        columns = ['bod1', 'bod31', 'cod1', 'cod31']
    
    columns = [col for col in columns if col in df.columns]
    
    return df[columns].std() / df[columns].mean()


def compute_all_statistics(
    results: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Compute statistics for all scenarios.
    
    Args:
        results: Dictionary mapping scenario names to DataFrames.
    
    Returns:
        Combined DataFrame with statistics for all scenarios.
    """
    all_stats = []
    
    for scenario_name, df in results.items():
        if df.empty:
            continue
        
        stats = compute_summary_stats(df)
        stats.columns = pd.MultiIndex.from_product(
            [[scenario_name], stats.columns]
        )
        all_stats.append(stats)
    
    if all_stats:
        return pd.concat(all_stats, axis=1)
    return pd.DataFrame()


def get_compliance_summary(
    results: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Generate compliance summary for all scenarios.
    
    Args:
        results: Dictionary mapping scenario names to DataFrames.
    
    Returns:
        DataFrame with compliance counts.
    """
    summary_data = []
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        row = {
            "Scenario": scenario_name,
            "Total Records": len(df),
            "Compliant": (df["fail_type"] == "Compliant").sum(),
            "LUT Exceedance": (df["fail_type"] == "LUT exceedance").sum(),
            "Max Limit Failure": (df["fail_type"] == "Max Limit Failure").sum(),
        }
        
        if "fail_source" in df.columns:
            row["BOD Source"] = (df["fail_source"] == "BOD").sum()
            row["COD Source"] = (df["fail_source"] == "COD").sum()
        
        summary_data.append(row)
    
    return pd.DataFrame(summary_data)


def compute_probability_exceedance(
    df: pd.DataFrame,
    column: str,
    threshold: float
) -> float:
    """
    Compute probability of exceeding a threshold.
    
    Args:
        df: DataFrame to analyse.
        column: Column name.
        threshold: Threshold value.
    
    Returns:
        Probability (0-1) of exceeding threshold.
    """
    if column not in df.columns:
        return 0.0
    
    count = (df[column] > threshold).sum()
    return count / len(df)


def compute_exceedance_analysis(
    results: Dict[str, pd.DataFrame]
) -> Dict[str, Dict[str, float]]:
    """
    Compute exceedance probabilities for all scenarios.
    
    Args:
        results: Dictionary mapping scenario names to DataFrames.
    
    Returns:
        Nested dictionary of exceedance probabilities.
    """
    thresholds = {
        'bod1': 300,   # BOD influent threshold
        'bod31': 50,   # BOD effluent threshold
        'cod1': 500,   # COD influent threshold
        'cod31': 250,  # COD effluent threshold
    }
    
    analysis = {}
    
    for scenario_name, df in results.items():
        if df.empty:
            continue
        
        scenario_probs = {}
        for column, threshold in thresholds.items():
            if column in df.columns:
                scenario_probs[f"prob_{column}_gt_{threshold}"] = (
                    compute_probability_exceedance(df, column, threshold)
                )
        
        analysis[scenario_name] = scenario_probs
    
    return analysis
