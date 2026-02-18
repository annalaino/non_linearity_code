"""
File helper utilities.

Common file and path operations.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path.
    
    Returns:
        Path object.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_path(
    filename: str,
    output_dir: Optional[Path] = None,
    timestamp: bool = False,
    suffix: str = ""
) -> Path:
    """
    Get a path for output files.
    
    Args:
        filename: Base filename.
        output_dir: Output directory. If None, uses current directory.
        timestamp: Whether to add timestamp to filename.
        suffix: Optional suffix to add before extension.
    
    Returns:
        Path object.
    """
    if output_dir is None:
        output_dir = Path.cwd()
    
    ensure_dir(output_dir)
    
    # Parse filename and extension
    if "." in filename:
        name, ext = filename.rsplit(".", 1)
        ext = f".{ext}"
    else:
        name = filename
        ext = ""
    
    # Add suffix if provided
    if suffix:
        name = f"{name}_{suffix}"
    
    # Add timestamp if requested
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"{name}_{ts}"
    
    return output_dir / f"{name}{ext}"


def get_data_path(relative_path: str, root: Path = None) -> Path:
    """
    Get absolute path to data file.
    
    Args:
        relative_path: Relative path from project root.
        root: Project root. If None, derived from this file.
    
    Returns:
        Absolute path.
    """
    if root is None:
        root = Path(__file__).parent.parent.parent
    
    return root / relative_path
