"""
Main processor module.

Orchestrates the full data processing pipeline.
"""

from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from ..config import ComplianceLimits, ProjectPaths, get_config, SCENARIOS
from ..data.loaders import load_pickle_file, process_folder
from ..data.validators import validate_dataframe, check_required_columns
from ..utils.logging_config import log
from .metrics import process_dataframe


def process_scenario(
    scenario_key: str,
    data_dir: Path,
    config: ComplianceLimits,
    output_dir: Optional[Path] = None,
    save_csv: bool = True
) -> pd.DataFrame:
    """
    Process a single scenario.
    
    Args:
        scenario_key: Key in SCENARIOS dict (e.g., 'baseline')
        data_dir: Path to data directory.
        config: Compliance limits.
        output_dir: Directory for CSV output.
        save_csv: Whether to save CSV files.
    
    Returns:
        Processed DataFrame.
    """
    folder_name = SCENARIOS.get(scenario_key, scenario_key)
    folder_path = data_dir / folder_name
    
    # Load raw data
    raw_df = process_folder(folder_path, config, save_csv=False)
    
    if raw_df.empty:
        return raw_df
    
    # Process through compliance calculations
    processed_df = process_dataframe(raw_df, config)
    
    # Save processed data
    if save_csv and output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(
            output_dir / f"{scenario_key}_processed.csv", 
            index=False
        )
    
    return processed_df


def run_full_analysis(
    root_path: Path = None,
    save_output: bool = True
) -> Dict[str, pd.DataFrame]:
    """
    Run the complete analysis pipeline for all scenarios.
    
    Args:
        root_path: Project root path. If None, auto-detected.
        save_output: Whether to save results to CSV.
    
    Returns:
        Dictionary mapping scenario keys to processed DataFrames.
    """
    config, paths = get_config(root_path)
    
    if save_output:
        paths.ensure_output_dirs()
    
    results = {}
    
    for scenario_key in SCENARIOS.keys():
        log.info(f"Processing scenario: {scenario_key}")
        
        df = process_scenario(
            scenario_key=scenario_key,
            data_dir=paths.data,
            config=config,
            output_dir=paths.csv_output if save_output else None,
            save_csv=save_output
        )
        
        if not df.empty:
            results[scenario_key] = df
    
    return results


def get_scenario_summary(
    results: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Generate summary statistics for all scenarios.
    
    Args:
        results: Dictionary of scenario DataFrames.
    
    Returns:
        Summary DataFrame.
    """
    summary_data = []
    
    for scenario_name, df in results.items():
        if df.empty or "fail_type" not in df.columns:
            continue
        
        row = {
            "Category": scenario_name,
            "Compliant Count": (df["fail_type"] == "Compliant").sum(),
            "LUT Exceedance Count": (df["fail_type"] == "LUT exceedance").sum(),
            "Max Limit Failure Count": (df["fail_type"] == "Max Limit Failure").sum(),
        }
        
        if "fail_source" in df.columns:
            row["BOD Source Count"] = (df["fail_source"] == "BOD").sum()
            row["COD Source Count"] = (df["fail_source"] == "COD").sum()
            row["Pass Source Count"] = (df["fail_source"] == "None").sum()
        
        if "c_BOD_2" in df.columns:
            row["BOD 2 Limit"] = (df["c_BOD_2"] == True).sum()
            row["BOD 3 Limit"] = (df["c_BOD_3"] == True).sum()
        
        summary_data.append(row)
    
    return pd.DataFrame(summary_data)
