"""Core inspection execution runner.

Owned by: MEMBER 3 (Inspection Logic) - Coordinated with MEMBER 1
"""

from typing import Optional
import numpy as np
import pandas as pd

from .result_models import CheckStatus, InspectionItemResult, InspectionSummary


def run_inspection(
    image: Optional[np.ndarray],
    checklist_df: pd.DataFrame,
) -> InspectionSummary:
    """Execute quality inspection checks against the checklist items.

    Parameters
    ----------
    image : Optional[np.ndarray]
        OpenCV BGR image of the cabinet, if uploaded.
    checklist_df : pd.DataFrame
        DataFrame containing checklist items with required columns:
        check_id, check_name, expected_value.

    Returns
    -------
    InspectionSummary
        Inspection summary populated with structured results.
    """
    has_demo_columns = any(col in checklist_df.columns for col in ["demo_status", "demo_found_value", "evidence_box"])

    if has_demo_columns:
        from src.eagle_eye.input_processing.file_loader import checklist_to_inspection_results
        results = checklist_to_inspection_results(checklist_df)
    else:
        results = []
        for _, row in checklist_df.iterrows():
            check_id = str(row.get("check_id", "UNKNOWN"))
            check_name = str(row.get("check_name", "Unnamed Check"))
            expected = str(row.get("expected_value", "N/A"))
            notes = str(row.get("notes", ""))

            # Baseline behavior: mark as Needs Manual Check pending concrete CV detection
            item = InspectionItemResult(
                check_id=check_id,
                check_name=check_name,
                expected_value=expected,
                found_value="Pending Verification",
                status=CheckStatus.MANUAL_CHECK,
                notes=f"Initial inspection baseline. {notes}".strip(),
                evidence_bbox=None,
                marker_id=None,
            )
            results.append(item)

    return InspectionSummary.from_items(results)
