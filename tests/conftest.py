"""
Pytest configuration and fixtures.

Common test fixtures for the test suite.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nonlinearity.config import ComplianceLimits


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        'bod1': [100, 150, 200, 250, 300],
        'bod31': [20, 25, 30, 35, 40],
        'cod1': [200, 300, 400, 500, 600],
        'cod31': [40, 50, 60, 70, 80],
        'snh1': [10, 15, 20, 25, 30],
        'snh31': [5, 7, 9, 11, 13],
    })


@pytest.fixture
def compliance_limits():
    """Create default compliance limits."""
    return ComplianceLimits()


@pytest.fixture
def processed_data(sample_data, compliance_limits):
    """Create processed DataFrame with all calculations."""
    from nonlinearity.core.metrics import process_dataframe
    
    return process_dataframe(sample_data, compliance_limits)
