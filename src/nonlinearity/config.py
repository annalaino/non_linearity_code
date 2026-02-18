"""
Configuration module for non-linearity analysis.

Contains all project constants, compliance limits, and path configurations.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class ComplianceLimits:
    """
    Compliance limits for BOD and COD analysis.
    
    All values are in mg/L unless otherwise specified.
    """
    bod_upper: float = 50
    bod_lower: float = 25
    cod_upper: float = 250
    cod_lower: float = 125
    bod_pc: float = 0.7  # BOD percentage
    cod_pc: float = 0.75  # COD percentage

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for legacy compatibility."""
        return {
            "bod_upper": self.bod_upper,
            "bod_lower": self.bod_lower,
            "cod_upper": self.cod_upper,
            "cod_lower": self.cod_lower,
            "bod_pc": self.bod_pc,
            "cod_pc": self.cod_pc,
        }


# Simulation parameters (separate from compliance limits)
class SimulationConfig:
    """Simulation configuration parameters."""
    
    # Time step in days (used for recovery time calculations)
    TIME_STEP: float = 0.08
    
    # Conversion factors
    HOURS_PER_DAY: int = 24
    MINUTES_PER_HOUR: int = 60


@dataclass
class ProjectPaths:
    """
    Project path configuration.
    
    Uses pathlib for cross-platform path handling.
    """
    root: Path
    
    @property
    def data(self) -> Path:
        """Path to data directory."""
        return self.root / "data"
    
    @property
    def output(self) -> Path:
        """Path to output directory."""
        return self.root / "output"
    
    @property
    def csv_output(self) -> Path:
        """Path to CSV output directory."""
        return self.output / "csv"
    
    @property
    def plots_output(self) -> Path:
        """Path to plots output directory."""
        return self.output / "plots"

    def ensure_output_dirs(self) -> None:
        """Create output directories if they don't exist."""
        self.csv_output.mkdir(parents=True, exist_ok=True)
        self.plots_output.mkdir(parents=True, exist_ok=True)


# Scenario configuration
SCENARIOS = {
    "baseline": "baseline",
    "130%": "1.3",
    "150%": "1.5",
    "190%": "1.9",
}

SCENARIO_LABELS = {
    "baseline": "Baseline",
    "130%": "Shift 130%",
    "150%": "Shift 150%",
    "190%": "Shift 190%",
}

# Required columns in input data
REQUIRED_COLUMNS = [
    'bod1', 'cod1', 'bod31', 'cod31', 'snh1', 'snh31'
]


def get_config(root_path: Path = None) -> tuple[ComplianceLimits, ProjectPaths]:
    """
    Get configuration based on the project root path.
    
    Args:
        root_path: Path to project root. Defaults to src/nonlinearity parent.
    
    Returns:
        Tuple of (ComplianceLimits, ProjectPaths)
    """
    if root_path is None:
        # Derive from this file's location
        root_path = Path(__file__).parent.parent.parent
    
    return (
        ComplianceLimits(),
        ProjectPaths(root=root_path)
    )


def get_scenario_path(scenario_key: str, config: ProjectPaths = None) -> Path:
    """
    Get the path to a scenario's data directory.
    
    Args:
        scenario_key: Key in SCENARIOS dict (e.g., 'baseline', '130%')
        config: ProjectPaths instance. If None, will be created.
    
    Returns:
        Path to the scenario's data directory
    """
    if config is None:
        _, config = get_config()
    
    folder_name = SCENARIOS.get(scenario_key, scenario_key)
    return config.data / folder_name
