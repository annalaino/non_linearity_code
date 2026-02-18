"""
Scatter plot functions.

Influent vs effluent concentration plots.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .plots import setup_matplotlib, save_figure


def plot_influent_effluent(
    results: Dict[str, pd.DataFrame],
    param: str,
    scenarios: List[str] = None,
    output_dir: Optional[Path] = None,
    save: bool = True,
    show: bool = True
) -> plt.Figure:
    """
    Plot influent vs effluent for a parameter (BOD or COD).
    
    Args:
        results: Dictionary of scenario DataFrames.
        param: Parameter name ('BOD' or 'COD').
        scenarios: List of scenario keys to plot. If None, uses all.
        output_dir: Directory to save plot.
        save: Whether to save the plot.
        show: Whether to display the plot.
    
    Returns:
        Matplotlib figure.
    """
    if scenarios is None:
        scenarios = list(results.keys())
    
    influent_col = f"{param.lower()}1"
    effluent_col = f"{param.lower()}31"
    
    n_scenarios = len(scenarios)
    n_cols = min(4, n_scenarios)
    n_rows = (n_scenarios + n_cols - 1) // n_cols
    
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 5*n_rows))
    fig.suptitle(f'{param} Influent vs Effluent')
    
    if n_scenarios == 1:
        axs = np.array([axs])
    axs = axs.flatten()
    
    for idx, scenario in enumerate(scenarios):
        df = results[scenario]
        
        if df.empty or influent_col not in df.columns:
            continue
        
        # Sort data
        influent_sorted = np.sort(df[influent_col])
        effluent_sorted = np.array(df[effluent_col])[
            np.argsort(df[influent_col])
        ]
        
        axs[idx].scatter(influent_sorted, effluent_sorted, alpha=0.5, s=10)
        axs[idx].set_xlabel('Influent')
        axs[idx].set_ylabel('Effluent')
        axs[idx].set_title(f'{param} ({scenario})')
        axs[idx].grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(n_scenarios, len(axs)):
        axs[idx].set_visible(False)
    
    plt.tight_layout()
    
    if save and output_dir:
        save_figure(fig, f"{param.lower()}_scatter.png", output_dir)
    
    if not show:
        plt.close(fig)
    
    return fig


def plot_all_scatter(
    results: Dict[str, pd.DataFrame],
    output_dir: Optional[Path] = None,
    save: bool = True
) -> Dict[str, plt.Figure]:
    """
    Plot all BOD and COD scatter plots.
    
    Args:
        results: Dictionary of scenario DataFrames.
        output_dir: Directory to save plots.
        save: Whether to save plots.
    
    Returns:
        Dictionary of figures.
    """
    figures = {}
    
    for param in ['BOD', 'COD']:
        fig = plot_influent_effluent(
            results, 
            param, 
            output_dir=output_dir, 
            save=save
        )
        figures[param] = fig
    
    return figures
