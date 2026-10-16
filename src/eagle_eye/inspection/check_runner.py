"""Core inspection execution runner.

Owned by: MEMBER 3 (Inspection Logic)
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

    NOTE: In this initialization phase, this runner serves as a clean starter
    interface. In subsequent development tasks, Member 3 and Member 2 will connect
    concrete rule-based verifications and visual detection routines here.

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
        Initial inspection summary populated with structured results.
    """
    results = []

    for _, row in checklist_df.iterrows():
        check_id = str(row.get("check_id", "UNKNOWN"))
        check_name = str(row.get("check_name", "Unnamed Check"))
        expected = str(row.get("expected_value", "N/A"))
        notes = str(row.get("notes", ""))

        # Starter stub behavior: mark as Needs Manual Check pending computer vision rule implementation
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
