"""
Tests for configuration module.
"""

import pytest
from nonlinearity.config import (
    ComplianceLimits,
    ProjectPaths,
    get_config,
    SCENARIOS,
    REQUIRED_COLUMNS
)


class TestComplianceLimits:
    """Tests for ComplianceLimits dataclass."""
    
    def test_default_values(self):
        """Test default compliance limits."""
        limits = ComplianceLimits()
        
        assert limits.bod_upper == 50
        assert limits.bod_lower == 25
        assert limits.cod_upper == 250
        assert limits.cod_lower == 125
        assert limits.bod_pc == 0.7
        assert limits.cod_pc == 0.75
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        limits = ComplianceLimits()
        d = limits.to_dict()
        
        assert isinstance(d, dict)
        assert d["bod_upper"] == 50
        assert d["cod_pc"] == 0.75


class TestProjectPaths:
    """Tests for ProjectPaths dataclass."""
    
    def test_paths(self, tmp_path):
        """Test path properties."""
        paths = ProjectPaths(root=tmp_path)
        
        assert paths.data == tmp_path / "data"
        assert paths.output == tmp_path / "output"
        assert paths.csv_output == tmp_path / "output" / "csv"
        assert paths.plots_output == tmp_path / "output" / "plots"
    
    def test_ensure_output_dirs(self, tmp_path):
        """Test output directory creation."""
        paths = ProjectPaths(root=tmp_path)
        paths.ensure_output_dirs()
        
        assert paths.csv_output.exists()
        assert paths.plots_output.exists()


class TestConstants:
    """Tests for module constants."""
    
    def test_scenarios(self):
        """Test scenario definitions."""
        assert "baseline" in SCENARIOS
        assert "130%" in SCENARIOS
        assert SCENARIOS["baseline"] == "baseline"
        assert SCENARIOS["130%"] == "1.3"
    
    def test_required_columns(self):
        """Test required columns list."""
        assert isinstance(REQUIRED_COLUMNS, list)
        assert "bod1" in REQUIRED_COLUMNS
        assert "cod31" in REQUIRED_COLUMNS


class TestGetConfig:
    """Tests for get_config function."""
    
    def test_get_config(self):
        """Test config retrieval."""
        limits, paths = get_config()
        
        assert isinstance(limits, ComplianceLimits)
        assert isinstance(paths, ProjectPaths)
