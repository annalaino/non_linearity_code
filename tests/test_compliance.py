"""
Tests for core compliance calculations.
"""

import pytest
import pandas as pd

from nonlinearity.core.compliance import (
    calculate_bod_limits,
    calculate_cod_limits,
    calculate_all_limits,
    calculate_flag_conditions,
    calculate_failure_conditions,
)


class TestCalculateBODLimits:
    """Tests for BOD limit calculations."""
    
    def test_bod_limits(self, sample_data, compliance_limits):
        """Test BOD limit calculations."""
        result = calculate_bod_limits(sample_data, compliance_limits)
        
        assert 'BODut' in result.columns
        assert 'BODlt' in result.columns
        assert len(result) == len(sample_data)


class TestCalculateCODLimits:
    """Tests for COD limit calculations."""
    
    def test_cod_limits(self, sample_data, compliance_limits):
        """Test COD limit calculations."""
        result = calculate_cod_limits(sample_data, compliance_limits)
        
        assert 'CODut' in result.columns
        assert 'CODlt' in result.columns
        assert len(result) == len(sample_data)


class TestCalculateAllLimits:
    """Tests for combined limit calculations."""
    
    def test_all_limits(self, sample_data, compliance_limits):
        """Test all limit calculations."""
        result = calculate_all_limits(sample_data, compliance_limits)
        
        assert 'BODut' in result.columns
        assert 'BODlt' in result.columns
        assert 'CODut' in result.columns
        assert 'CODlt' in result.columns


class TestFlagConditions:
    """Tests for flag condition calculations."""
    
    def test_flag_conditions(self, processed_data):
        """Test flag conditions."""
        result = calculate_flag_conditions(processed_data)
        
        assert 'flag_BODlt' in result.columns
        assert 'flag_BODut' in result.columns
        assert 'flag_CODlt' in result.columns
        assert 'flag_CODut' in result.columns
