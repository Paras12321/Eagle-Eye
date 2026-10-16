# EAGLE EYE — System Architecture

## 1. Architectural Philosophy

EAGLE EYE is designed as a **lightweight, modular Python application**. It prioritizes clarity, maintainability, and rapid developer iteration during the hackathon. 

To keep the application accessible and deterministic:
- **No Heavy Backend / Microservices**: The entire demonstration operates within a unified Python environment.
- **No Cloud Database / Authentication**: Local data structures and memory state in Streamlit handle the interactive session.
- **Clear Module Decoupling**: Each sub-domain (input, vision, inspection, reporting, re-inspection) resides in its own isolated package under `src/eagle_eye/` with explicit input/output contracts.

---

## 2. Planned Data & Execution Flow

```text
User
  │
  ▼
Streamlit Interface (app.py)
  │
  ▼
Input Processing (src/eagle_eye/input_processing)
  │  - Image file validation (JPG / PNG)
  │  - Checklist validation & parsing (CSV / Excel)
  │
  ▼
Inspection Runner (src/eagle_eye/inspection/check_runner.py)
  │
  ├──► Basic Vision & Evidence Annotation (src/eagle_eye/vision/)
  │      - Image decoding & aspect ratio scaling
  │      - Bounding box rendering & numbered issue markers
  │
  ├──► Inspection Results (src/eagle_eye/inspection/result_models.py)
  │      - CheckStatus evaluation (PASS / FAIL / Needs Manual Check)
  │      - Aggregation into InspectionSummary
  │
  ├──► Report Generation (src/eagle_eye/reporting/report_generator.py)
  │      - Tabular summary formatting
  │      - Export to CSV and Markdown
  │
  └──► Demo Re-inspection (src/eagle_eye/reinspection/demo_recheck.py)
         - Simulated component repair verification
         - Updated InspectionSummary calculation
  │
  ▼
Results Displayed to User (Streamlit UI)
```

---

## 3. Package & Module Organization

| Module / Package | Directory | Primary Role |
|---|---|---|
| **Configuration** | `config/settings.py` | Project paths, supported file extensions, metadata. |
| **Input Processing** | `src/eagle_eye/input_processing/` | Validates file formats and parses CSV/Excel checklists into DataFrames. |
| **Computer Vision** | `src/eagle_eye/vision/` | OpenCV decoding, aspect-ratio resizing, bounding boxes, and numbered issue markers. |
| **Inspection Logic** | `src/eagle_eye/inspection/` | Result data models (`CheckStatus`, `InspectionSummary`) and execution runner. |
| **Reporting** | `src/eagle_eye/reporting/` | Formats results into DataFrames, exports CSV reports and Markdown summaries. |
| **Re-inspection** | `src/eagle_eye/reinspection/` | Handles demonstration fix simulation and status updates. |
| **User Interface** | `app.py` | Streamlit web application orchestrating user interactions and visualizations. |
| **Testing** | `tests/` | Unit test suite verifying loading, data models, annotations, and helpers. |

---

## 4. Shared Data Contracts

The central shared object between modules is `InspectionSummary` defined in `src/eagle_eye/inspection/result_models.py`:

```python
class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    MANUAL_CHECK = "Needs Manual Check"

@dataclass
class InspectionItemResult:
    check_id: str
    check_name: str
    expected_value: str
    found_value: Optional[str]
    status: CheckStatus
    notes: str
    evidence_bbox: Optional[Tuple[int, int, int, int]]
    marker_id: Optional[int]

@dataclass
class InspectionSummary:
    total_checks: int
    passed_count: int
    failed_count: int
    manual_check_count: int
    items: List[InspectionItemResult]
```

Any changes to these fields must be coordinated across the team to preserve interface compatibility.
