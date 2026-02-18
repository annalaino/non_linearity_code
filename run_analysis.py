#!/usr/bin/env python
"""
Main analysis runner script.

Run the complete non-linearity analysis pipeline.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nonlinearity.config import get_config
from nonlinearity.core.processors import run_full_analysis, get_scenario_summary
from nonlinearity.analysis.statistics import get_compliance_summary
from nonlinearity.analysis.nonstationarity import compute_nonstationarity_table
from nonlinearity.analysis.recovery import get_recovery_analysis
from nonlinearity.visualisation.scatter import plot_all_scatter
from nonlinearity.visualisation.histograms import plot_all_concentration_histograms
from nonlinearity.visualisation.charts import (
    plot_comparison_bars, 
    plot_recovery_histogram,
    plot_mean_recovery_time,
    plot_metric_histogram
)
from nonlinearity.utils.logging_config import setup_logging, log


def main():
    """Run the complete analysis pipeline."""
    # Setup logging
    setup_logging(level="INFO")
    
    log.info("=" * 60)
    log.info("Non-Linearity Analysis Pipeline")
    log.info("=" * 60)
    
    # Get configuration
    config, paths = get_config()
    
    log.info(f"Project root: {paths.root}")
    log.info(f"Data directory: {paths.data}")
    log.info(f"Output directory: {paths.output}")
    
    # Ensure output directories exist
    paths.ensure_output_dirs()
    
    # Run analysis
    log.info("")
    log.info("=" * 60)
    log.info("Step 1: Processing Data")
    log.info("=" * 60)
    
    results = run_full_analysis(save_output=True)
    
    log.info(f"Processed {len(results)} scenarios:")
    for name in results.keys():
        log.info(f"  - {name}: {len(results[name])} records")
    
    # Generate summary
    log.info("")
    log.info("=" * 60)
    log.info("Step 2: Compliance Summary")
    log.info("=" * 60)
    
    summary = get_compliance_summary(results)
    log.info("\n" + summary.to_string(index=False))
    
    # Save summary
    summary.to_csv(paths.csv_output / "compliance_summary.csv", index=False)
    log.info(f"Saved: {paths.csv_output / 'compliance_summary.csv'}")
    
    # Non-stationarity analysis
    log.info("")
    log.info("=" * 60)
    log.info("Step 3: Non-Stationarity Analysis")
    log.info("=" * 60)
    
    ns_table = compute_nonstationarity_table(results)
    log.info("\n" + ns_table.to_string(index=False))
    ns_table.to_csv(paths.csv_output / "nonstationarity.csv", index=False)
    
    # Recovery analysis
    log.info("")
    log.info("=" * 60)
    log.info("Step 4: Recovery Time Analysis")
    log.info("=" * 60)
    
    recovery = get_recovery_analysis(results)
    log.info("\n" + recovery.to_string(index=False))
    recovery.to_csv(paths.csv_output / "recovery_analysis.csv", index=False)
    
    # Generate plots
    log.info("")
    log.info("=" * 60)
    log.info("Step 5: Generating Plots")
    log.info("=" * 60)
    
    plot_all_scatter(results, output_dir=paths.plots_output, save=True)
    plot_all_concentration_histograms(results, output_dir=paths.plots_output, save=True)
    plot_comparison_bars(results, output_dir=paths.plots_output, save=True)
    plot_recovery_histogram(results, output_dir=paths.plots_output, save=True)
    plot_mean_recovery_time(results, output_dir=paths.plots_output, save=True)
    plot_metric_histogram(results, bins=30, output_dir=paths.plots_output, save=True)
    
    log.info("")
    log.info("=" * 60)
    log.info("Analysis Complete!")
    log.info("=" * 60)
    log.info("")
    log.info(f"Results saved to: {paths.output}")
    log.info(f"  - CSV files: {paths.csv_output}")
    log.info(f"  - Plots: {paths.plots_output}")
    
    return results


if __name__ == "__main__":
    main()
