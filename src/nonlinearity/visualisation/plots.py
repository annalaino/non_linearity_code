"""
Base plotting utilities.

Common setup and helper functions for matplotlib.
"""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from ..utils.logging_config import log


def setup_matplotlib(figsize: tuple = (10, 6)) -> tuple:
    """
    Setup matplotlib figure and axis.
    
    Args:
        figsize: Figure size as (width, height).
    
    Returns:
        Tuple of (figure, axis).
    """
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def save_figure(
    fig,
    filename: str,
    output_dir: Optional[Path] = None,
    dpi: int = 150,
    bbox_inches: str = 'tight'
) -> Path:
    """
    Save figure to file.
    
    Args:
        fig: Matplotlib figure.
        filename: Output filename.
        output_dir: Output directory. If None, uses current directory.
        dpi: Resolution in dots per inch.
        bbox_inches: Bounding box setting.
    
    Returns:
        Path to saved file.
    """
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
    else:
        filepath = Path(filename)
    
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    log.info(f"Saved figure: {filepath}")
    
    return filepath


def close_figure(fig):
    """Close figure to free memory."""
    plt.close(fig)
