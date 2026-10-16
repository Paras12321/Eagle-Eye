"""Data structures and status enumerations for inspection results.

Owned by: MEMBER 3 (Inspection Logic)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple, Dict, Any


class CheckStatus(str, Enum):
    """Quality check statuses supported by Eagle Eye."""
    PASS = "PASS"
    FAIL = "FAIL"
    MANUAL_CHECK = "Needs Manual Check"


@dataclass
class InspectionItemResult:
    """Inspection outcome for a single checklist line item."""
    check_id: str
    check_name: str
    expected_value: str
    found_value: Optional[str] = None
    status: CheckStatus = CheckStatus.MANUAL_CHECK
    notes: str = ""
    evidence_bbox: Optional[Tuple[int, int, int, int]] = None
    marker_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the item result to a serializable dictionary."""
        return {
            "check_id": self.check_id,
            "check_name": self.check_name,
            "expected_value": self.expected_value,
            "found_value": self.found_value if self.found_value is not None else "N/A",
            "status": self.status.value,
            "notes": self.notes,
            "has_evidence": self.evidence_bbox is not None or self.marker_id is not None,
        }


@dataclass
class InspectionSummary:
    """Aggregated summary of an inspection run."""
    total_checks: int
    passed_count: int
    failed_count: int
    manual_check_count: int
    items: List[InspectionItemResult] = field(default_factory=list)

    @classmethod
    def from_items(cls, items: List[InspectionItemResult]) -> "InspectionSummary":
        """Construct an InspectionSummary by aggregating item results."""
        total = len(items)
        passed = sum(1 for item in items if item.status == CheckStatus.PASS)
        failed = sum(1 for item in items if item.status == CheckStatus.FAIL)
        manual = sum(1 for item in items if item.status == CheckStatus.MANUAL_CHECK)
        return cls(
            total_checks=total,
            passed_count=passed,
            failed_count=failed,
            manual_check_count=manual,
            items=items,
        )

    def is_overall_pass(self) -> bool:
        """Return True if all items passed with zero failures or manual checks."""
        return self.total_checks > 0 and self.passed_count == self.total_checks

    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary format for reporting."""
        return {
            "total_checks": self.total_checks,
            "passed_count": self.passed_count,
            "failed_count": self.failed_count,
            "manual_check_count": self.manual_check_count,
            "overall_status": "PASS" if self.is_overall_pass() else "ACTION_REQUIRED",
            "items": [item.to_dict() for item in self.items],
        }
