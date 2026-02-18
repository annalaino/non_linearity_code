"""
Chart plotting functions.

Bar charts and line plots.
"""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..utils.logging_config import log


def plot_comparison_bars(
    results: Dict[str, pd.DataFrame],
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True
) -> plt.Figure:
    """
    Plot bar chart comparing compliance across scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
    
    Returns:
        Matplotlib figure.
    """
    # Collect data
    categories = []
    compliant = []
    lut = []
    max_lim = []
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        categories.append(scenario_name)
        compliant.append((df["fail_type"] == "Compliant").sum())
        lut.append((df["fail_type"] == "LUT exceedance").sum())
        max_lim.append((df["fail_type"] == "Max Limit Failure").sum())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(categories))
    width = 0.25
    
    ax.bar(x - width, compliant, width, label='Compliant')
    ax.bar(x, lut, width, label='LUT Exceedance')
    ax.bar(x + width, max_lim, width, label='Max Limit Failure')
    
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Count')
    ax.set_title('Compliance Comparison Across Scenarios')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "compliance_comparison.png"
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        log.info(f"Saved: {filepath}")
    
    if not show:
        plt.close(fig)
    
    return fig


def plot_recovery_histogram(
    results: Dict[str, pd.DataFrame],
    time_step: float = None,
    bins: int = 20,
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True
) -> plt.Figure:
    """
    Plot histogram of recovery times across scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
        time_step: Time step for conversion to minutes (default: 0.08 days).
        bins: Number of histogram bins.
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
    
    Returns:
        Matplotlib figure.
    """
    from ..analysis.recovery import compute_recovery_time_minutes
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        recovery_times = compute_recovery_time_minutes(df["fail_type"], time_step)
        
        ax.hist(
            recovery_times, 
            bins=bins, 
            alpha=0.5, 
            label=f'{scenario_name}'
        )
    
    ax.set_xlabel('Recovery Time (Minutes)')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Recovery Times')
    ax.legend()
    ax.set_ylim(0, 10)
    
    plt.tight_layout()
    
    if save and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "recovery_histogram.png"
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        log.info(f"Saved: {filepath}")
    
    if not show:
        plt.close(fig)
    
    return fig


def plot_mean_recovery_time(
    results: Dict[str, pd.DataFrame],
    time_step: float = None,
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True
) -> plt.Figure:
    """
    Plot mean recovery time line chart.
    
    Args:
        results: Dictionary of scenario DataFrames.
        time_step: Time step for conversion (default: 0.08 days).
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
    
    Returns:
        Matplotlib figure.
    """
    from ..analysis.recovery import compute_mean_recovery_time
    
    scenarios = []
    mean_times = []
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        scenarios.append(scenario_name)
        mean_times.append(compute_mean_recovery_time(df["fail_type"], time_step))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(scenarios, mean_times, marker='o')
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Average Recovery Time (minutes)')
    ax.set_title('Mean Recovery Time Across Scenarios')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Annotate points
    for x, y in zip(scenarios, mean_times):
        ax.text(x, y, f'{y:.1f} min', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "mean_recovery.png"
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        log.info(f"Saved: {filepath}")
    
    if not show:
        plt.close(fig)
    
    return fig


def plot_metric_histogram(
    results: Dict[str, pd.DataFrame],
    bins: int = 50,
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True,
    xlim: tuple = None
) -> plt.Figure:
    """
    Plot histogram of metric values across scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
        bins: Number of histogram bins.
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
        xlim: X-axis limits as (min, max).
    
    Returns:
        Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for scenario_name, df in results.items():
        if df.empty or "metric" not in df.columns:
            continue
        
        ax.hist(
            df["metric"], 
            bins=bins, 
            alpha=0.5, 
            label=f'{scenario_name}'
        )
    
    ax.set_xlabel('Metric')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Metric Values Across Scenarios')
    ax.legend()
    
    if xlim:
        ax.set_xlim(xlim)
    
    plt.tight_layout()
    
    if save and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "metric_histogram.png"
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        log.info(f"Saved: {filepath}")
    
    if not show:
        plt.close(fig)
    
    return fig
