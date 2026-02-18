"""Analysis modules for statistics and metrics."""

from .statistics import (
    compute_summary_stats,
    compute_cv,
    compute_all_statistics,
)
from .nonstationarity import non_stationarity_score
from .recovery import compute_recovery_time

__all__ = [
    "compute_summary_stats",
    "compute_cv",
    "compute_all_statistics",
    "non_stationarity_score",
    "compute_recovery_time",
]
