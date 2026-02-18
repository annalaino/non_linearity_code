"""
Non-linearity Analysis Package

A modular Python project for analysing BOD/COD compliance and non-stationarity
in wastewater treatment simulation data.
"""

__version__ = "0.1.0"

from .config import ComplianceLimits, ProjectPaths, get_config

__all__ = ["ComplianceLimits", "ProjectPaths", "get_config"]
