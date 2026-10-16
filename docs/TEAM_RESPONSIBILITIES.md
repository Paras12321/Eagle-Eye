# EAGLE EYE — Team Roles & Responsibilities

This document defines the proposed ownership areas for our 4-member hackathon team. Clear division of responsibilities ensures rapid parallel development while preventing git conflicts and broken dependencies.

---

## 1. Member Allocations

### 👤 MEMBER 1 — Input Processing & Validation
- **Primary Modules**: `src/eagle_eye/input_processing/`, `sample_data/`
- **Key Responsibilities**:
  - Implement robust file intake for cabinet images (`.jpg`, `.jpeg`, `.png`).
  - Implement checklist ingestion supporting both CSV and Excel (`.xlsx`) files.
  - Implement file format validation, file size limits, and user error messaging.
  - Maintain the official sample checklist format (`sample_data/checklist_template.csv`) with required columns (`check_id`, `check_name`, `expected_value`).
  - Author and maintain unit tests in `tests/test_file_loader.py`.

---

### 👤 MEMBER 2 — Computer Vision & Evidence Annotation
- **Primary Modules**: `src/eagle_eye/vision/`
- **Key Responsibilities**:
  - Image decoding from raw byte buffers and file paths using OpenCV.
  - Aspect-ratio resizing and standard display normalization for the Streamlit UI.
  - Implement bounding box drawing routines with colored borders and text labels.
  - Implement numbered circular visual issue markers (`draw_issue_marker`).
  - Extract cropped component regions for detailed inspection evidence view.
  - Author and maintain unit tests in `tests/test_annotation.py`.

---

### 👤 MEMBER 3 — Inspection Logic & Result Models
- **Primary Modules**: `src/eagle_eye/inspection/`
- **Key Responsibilities**:
  - Define and maintain core data structures (`CheckStatus`, `InspectionItemResult`, `InspectionSummary`).
  - Implement rule-based verification logic comparing expected checklist values against detected or extracted findings.
  - Standardize status categorization:
    - **`PASS`**: Expected component/state verified with high confidence.
    - **`FAIL`**: Discrepancy confirmed (e.g. missing breaker, incorrect terminal range).
    - **`Needs Manual Check`**: Inconclusive visual evidence requiring human inspector sign-off.
  - Author and maintain unit tests in `tests/test_check_runner.py`.

---

### 👤 MEMBER 4 — UI, Reporting & System Integration
- **Primary Modules**: `app.py`, `src/eagle_eye/reporting/`, `src/eagle_eye/reinspection/`
- **Key Responsibilities**:
  - Build and refine the interactive Streamlit user interface in `app.py`.
  - Connect modules from Members 1, 2, and 3 into an intuitive single-page or multi-tab workflow.
  - Implement export routines for audit-ready CSV reports and formatted Markdown summaries.
  - Build the simulated re-inspection demonstration (`demo_recheck.py`) showing a defect fix transition (`FAIL` -> `PASS`).
  - Coordinate end-to-end user testing and final demo readiness.

---

## 2. Shared Interfaces & Coordination Protocol

To avoid merge conflicts and breaking changes during development:

1. **Shared Contract Immunity**:
   - `src/eagle_eye/inspection/result_models.py` (`InspectionItemResult`, `InspectionSummary`, `CheckStatus`) and `config/settings.py` are **shared interfaces**.
   - No team member may alter field names, types, or return signatures in these files without prior agreement from all other team members.

2. **Branching & PR Workflow**:
   - Each member should work on a dedicated feature branch:
     - Member 1: `feature/input-processing`
     - Member 2: `feature/vision-annotations`
     - Member 3: `feature/inspection-logic`
     - Member 4: `feature/ui-integration`
   - Test suites must be executed (`pytest -q`) before submitting pull requests or merging into `main`.

3. **Adjustment**:
   - These ownership areas are baseline guidelines. The team can adjust responsibilities during the hackathon as needs evolve.
