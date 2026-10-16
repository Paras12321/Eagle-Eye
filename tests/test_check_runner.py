"""Unit tests for inspection data models and runner.

Owned by: MEMBER 3 (Inspection Logic)
"""

import pandas as pd
from src.eagle_eye.inspection.result_models import (
    CheckStatus,
    InspectionItemResult,
    InspectionSummary,
)
from src.eagle_eye.inspection.check_runner import run_inspection


def test_inspection_summary_counts():
    """Verify that InspectionSummary aggregates statuses accurately."""
    items = [
        InspectionItemResult("CHK-1", "Breaker Q1", "Present", "Present", CheckStatus.PASS),
        InspectionItemResult("CHK-2", "Terminal 1", "TB-01", "Missing", CheckStatus.FAIL),
        InspectionItemResult("CHK-3", "Earth Wire", "PE Green", None, CheckStatus.MANUAL_CHECK),
    ]
    summary = InspectionSummary.from_items(items)

    assert summary.total_checks == 3
    assert summary.passed_count == 1
    assert summary.failed_count == 1
    assert summary.manual_check_count == 1
    assert summary.is_overall_pass() is False


def test_inspection_summary_all_pass():
    """Verify that is_overall_pass() returns True when all checks pass."""
    items = [
        InspectionItemResult("CHK-1", "Breaker Q1", "Present", "Present", CheckStatus.PASS),
        InspectionItemResult("CHK-2", "Terminal 1", "TB-01", "TB-01", CheckStatus.PASS),
    ]
    summary = InspectionSummary.from_items(items)
    assert summary.is_overall_pass() is True


def test_run_inspection_baseline():
    """Verify that the baseline runner processes a DataFrame and returns an InspectionSummary."""
    df = pd.DataFrame([
        {"check_id": "CHK-01", "check_name": "Breaker", "expected_value": "Installed"},
        {"check_id": "CHK-02", "check_name": "Label", "expected_value": "L1"},
    ])
    summary = run_inspection(image=None, checklist_df=df)

    assert summary.total_checks == 2
    assert summary.manual_check_count == 2
    assert len(summary.items) == 2
    assert summary.items[0].check_id == "CHK-01"
