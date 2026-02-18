"""
Histogram plotting functions.

Concentration distribution plots.
"""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..utils.logging_config import log


def plot_concentration_histogram(
    results: Dict[str, pd.DataFrame],
    column: str,
    threshold: float,
    label_prefix: str = "",
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True,
    bins: int = 50,
    xlim: tuple = None
) -> plt.Figure:
    """
    Plot histogram of concentration values across scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
        column: Column name to plot.
        threshold: Threshold value to mark on plot.
        label_prefix: Prefix for legend labels.
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
        bins: Number of histogram bins.
        xlim: X-axis limits as (min, max).
    
    Returns:
        Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for scenario_name, df in results.items():
        if df.empty or column not in df.columns:
            continue
        
        # Calculate probability
        count_above = (df[column] > threshold).sum()
        prob = count_above / len(df[column])
        
        ax.hist(
            df[column], 
            bins=bins, 
            density=True, 
            alpha=0.5, 
            label=f'{label_prefix} {scenario_name} (Prob > {threshold} = {prob:.2f})'
        )
    
    # Add threshold line
    ax.axvline(x=threshold, color='r', linestyle='--', linewidth=1)
    
    ax.set_xlabel(f'{column} concentrations')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Histogram of {column} for all scenarios')
    ax.legend()
    
    if xlim:
        ax.set_xlim(xlim)
    
    plt.tight_layout()
    
    if save and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / f"histogram_{column}.png"
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        log.info(f"Saved: {filepath}")
    
    if not show:
        plt.close(fig)
    
    return fig


def plot_all_concentration_histograms(
    results: Dict[str, pd.DataFrame],
    output_dir: Optional[Path] = None,
    save: bool = True
) -> Dict[str, plt.Figure]:
    """
    Plot all concentration histograms.
    
    Args:
        results: Dictionary of scenario DataFrames.
        output_dir: Directory to save plots.
        save: Whether to save plots.
    
    Returns:
        Dictionary of figures.
    """
    figures = {}
    
    # Define columns and thresholds
    configs = [
        ('bod1', 300, 'BOD infl'),
        ('bod31', 50, 'BOD effl'),
        ('cod1', 500, 'COD infl'),
        ('cod31', 250, 'COD effl'),
    ]
    
    for column, threshold, label in configs:
        fig = plot_concentration_histogram(
            results, 
            column, 
            threshold,
            label_prefix=label,
            output_dir=output_dir,
            save=save,
            xlim=(0, threshold * 2) if 'effl' in column else None
        )
        figures[column] = fig
    
    return figures
