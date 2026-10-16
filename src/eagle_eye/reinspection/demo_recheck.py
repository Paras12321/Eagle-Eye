"""Re-inspection and fix verification utilities for demonstration.

Owned by: MEMBER 4 (UI, Reporting and Integration)
"""

from copy import deepcopy
from typing import Optional

from src.eagle_eye.inspection.result_models import CheckStatus, InspectionSummary


def simulate_reinspection_fix(
    original_summary: InspectionSummary,
    target_check_id: str,
    fixed_found_value: Optional[str] = None,
    resolution_note: str = "Resolved during re-inspection.",
) -> InspectionSummary:
    """Simulate a re-inspection fix on a failing or flagged checklist item.

    This function produces an updated InspectionSummary reflecting the
    re-inspected state, intended for demonstration of the closed-loop
    inspection workflow.

    Parameters
    ----------
    original_summary : InspectionSummary
        The previous inspection summary.
    target_check_id : str
        The check_id to mark as resolved/passed.
    fixed_found_value : Optional[str]
        The verified found value. If None, the expected_value is copied.
    resolution_note : str
        Explanatory note for the re-inspection record.

    Returns
    -------
    InspectionSummary
        New InspectionSummary with updated item status and recalculation.
    """
    new_items = deepcopy(original_summary.items)

    for item in new_items:
        if item.check_id == target_check_id:
            item.status = CheckStatus.PASS
            item.found_value = fixed_found_value if fixed_found_value is not None else item.expected_value
            item.notes = f"{item.notes} | [RE-INSPECTED: {resolution_note}]".strip(" |")

    return InspectionSummary.from_items(new_items)
