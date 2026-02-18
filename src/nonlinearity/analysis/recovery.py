"""
Recovery time analysis functions.

Extracts recovery time computation from the original notebook.
"""

from typing import List

import pandas as pd
import numpy as np

from ..config import SimulationConfig


def compute_recovery_time(
    series: pd.Series,
    time_step: float = None,
    failure_types: tuple = ('Max Limit Failure', 'LUT exceedance')
) -> List[float]:
    """
    Compute recovery times from non-compliance periods.
    
    A recovery time is the duration from the end of a non-compliance 
    period back to compliance.
    
    Args:
        series: Series containing failure type values.
        time_step: Time step in simulation units (default: 0.08 days).
        failure_types: Tuple of values considered as failures/non-compliance.
    
    Returns:
        List of recovery times (in time_step units).
    """
    if time_step is None:
        time_step = SimulationConfig.TIME_STEP
    
    recovery_times = []
    non_compliance_duration = 0
    in_non_compliance = False
    
    for failure_type in series:
        if failure_type in failure_types:
            if not in_non_compliance:
                in_non_compliance = True
            non_compliance_duration += 1
        else:
            if in_non_compliance:
                recovery_time = round(non_compliance_duration * time_step, 2)
                recovery_times.append(recovery_time)
                non_compliance_duration = 0
                in_non_compliance = False
    
    # Check for ongoing non-compliance at the end of the series
    if in_non_compliance:
        recovery_time = round(non_compliance_duration * time_step, 2)
        recovery_times.append(recovery_time)
    
    return recovery_times


def compute_recovery_time_minutes(
    series: pd.Series,
    time_step: float = None
) -> List[float]:
    """
    Compute recovery times and convert to minutes.
    
    Args:
        series: Series containing failure type values.
        time_step: Time step in simulation units (default: 0.08 days).
    
    Returns:
        List of recovery times in minutes.
    """
    if time_step is None:
        time_step = SimulationConfig.TIME_STEP
    
    recovery_times = compute_recovery_time(series, time_step)
    
    # Convert to minutes (time_step is in days, recovery_times already scaled)
    return [
        time * SimulationConfig.HOURS_PER_DAY * SimulationConfig.MINUTES_PER_HOUR
        for time in recovery_times
    ]


def compute_mean_recovery_time(
    series: pd.Series,
    time_step: float = None,
    convert_to_minutes: bool = True
) -> float:
    """
    Compute mean recovery time.
    
    Args:
        series: Series containing failure type values.
        time_step: Time step in simulation units (default: 0.08 days).
        convert_to_minutes: Whether to convert to minutes.
    
    Returns:
        Mean recovery time.
    """
    if convert_to_minutes:
        times = compute_recovery_time_minutes(series, time_step)
    else:
        times = compute_recovery_time(series, time_step)
    
    if not times:
        return 0.0
    
    return float(np.mean(times))


def get_recovery_analysis(
    results: dict,
    time_step: float = None
) -> pd.DataFrame:
    """
    Compute recovery time analysis for all scenarios.
    
    Args:
        results: Dictionary mapping scenario names to DataFrames.
        time_step: Time step in simulation units (default: 0.08 days).
    
    Returns:
        DataFrame with recovery time statistics.
    """
    rows = []
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        recovery_times_minutes = compute_recovery_time_minutes(
            df["fail_type"], 
            time_step,
        )
        
        if recovery_times_minutes:
            rows.append({
                "Scenario": scenario_name,
                "Mean Recovery (min)": np.mean(recovery_times_minutes),
                "Std Recovery (min)": np.std(recovery_times_minutes),
                "Min Recovery (min)": np.min(recovery_times_minutes),
                "Max Recovery (min)": np.max(recovery_times_minutes),
                "Num Events": len(recovery_times_minutes),
            })
    
    return pd.DataFrame(rows)
