"""
Data loading functions for pickle files and scenario data.

This module extracts the data loading logic from the original notebook.
"""

import os
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from ..config import ComplianceLimits, SCENARIOS
from ..utils.logging_config import log


def load_pickle_file(file_path: Path) -> Optional[pd.DataFrame]:
    """
    Load a single pickle file.
    
    Args:
        file_path: Path to the pickle file.
    
    Returns:
        DataFrame if successful, None if file is empty or corrupted.
    """
    try:
        df = pd.read_pickle(file_path)
        return df
    except pd.errors.EmptyDataError:
        log.warning(f"Empty DataFrame in file {file_path}")
        return None
    except Exception as e:
        log.warning(f"Error loading file {file_path}: {e}")
        return None


def process_folder(
    folder_path: Path,
    compliance_limits: ComplianceLimits,
    save_csv: bool = True,
    output_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Process all pickle files in a folder.
    
    This function extracts and processes all profile_run_*.pkl files
    from the specified folder, combining them into a single DataFrame.
    
    Args:
        folder_path: Path to the folder containing pickle files.
        compliance_limits: Compliance limits for calculations.
        save_csv: Whether to save individual CSV files.
        output_dir: Directory for CSV output. If None, saves to folder_path.
    
    Returns:
        Combined DataFrame with all processed data.
    """
    data_folder = []
    
    # Handle both string and Path inputs
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    
    if not folder_path.exists():
        log.warning(f"Folder {folder_path} does not exist")
        return pd.DataFrame()
    
    for filename in os.listdir(folder_path):
        # Skip non-Pickle files
        if not filename.endswith(".pkl"):
            continue
        
        file_path = folder_path / filename
        
        data_file = load_pickle_file(file_path)
        
        if data_file is None:
            continue
        
        if data_file.empty:
            log.warning(f"Empty DataFrame in file {file_path}")
            continue
        
        # Append to accumulated data
        data_folder.append(data_file)
        
        # Save individual file CSV if requested
        if save_csv:
            csv_name = file_path.stem  # filename without extension
            output_path = output_dir if output_dir else folder_path
            data_file.to_csv(output_path / f"{csv_name}.csv", index=False)
    
    # Return the concatenated results from all the files in the folder
    if not data_folder:
        log.warning(f"No data to return for folder {folder_path}")
        return pd.DataFrame()
    
    result_df = pd.concat(data_folder, ignore_index=True)
    
    # Save full combined CSV
    if save_csv and output_dir:
        csv_name = folder_path.name
        result_df.to_csv(output_dir / f"{csv_name}_full.csv", index=False)
    
    return result_df


def load_all_scenarios(
    compliance_limits: ComplianceLimits,
    data_dir: Path,
    output_dir: Optional[Path] = None
) -> Dict[str, pd.DataFrame]:
    """
    Load and process all scenario folders.
    
    Args:
        compliance_limits: Compliance limits for calculations.
        data_dir: Path to the data directory containing scenario subfolders.
        output_dir: Optional output directory for CSV files.
    
    Returns:
        Dictionary mapping scenario names to processed DataFrames.
    """
    results = {}
    
    for scenario_key, folder_name in SCENARIOS.items():
        folder_path = data_dir / folder_name
        log.info(f"Processing scenario: {scenario_key} ({folder_path})")
        
        df = process_folder(
            folder_path, 
            compliance_limits,
            save_csv=True,
            output_dir=output_dir
        )
        
        if not df.empty:
            results[scenario_key] = df
        else:
            log.warning(f"No data loaded for scenario {scenario_key}")
    
    return results


def get_data_summary(results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a summary table of compliance statistics for all scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
    
    Returns:
        DataFrame with summary statistics.
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
            row["Pass Source"] = (df["fail_source"] == "None").sum()
        
        summary_data.append(row)
    
    return pd.DataFrame(summary_data)
