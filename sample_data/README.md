# EAGLE EYE — Sample Data & Input Specification

This directory houses synthetic, sanitized sample data for testing and demonstrating the **EAGLE EYE** control cabinet quality inspection prototype.

---

## 1. Privacy and Data Governance Policy

> [!IMPORTANT]
> **Never commit real proprietary or confidential client data to this repository.**
> - Do **NOT** commit confidential industrial cabinet photographs.
> - Do **NOT** commit client engineering CAD drawings (`.dwg`, `.dxf`, `.pdf`).
> - Do **NOT** commit actual production spreadsheets containing proprietary part codes, serial numbers, or customer names.
> - All demo files committed here are **100% synthetic, sanitized, or mock graphics**.

---

## 2. Supported Input Formats

### 📷 Cabinet Photographs
- **File Extensions**: `.jpg`, `.jpeg`, `.png` (case-insensitive).
- **Validation**:
  - Image files must decode into a valid 3-channel (BGR) array with non-zero dimensions.
  - Corrupted, empty (0 bytes), or non-image formats are rejected with descriptive error notifications.
- **Sample File**: [`sample_data/sample_cabinet.png`](sample_cabinet.png) (A synthetic 960x680 px industrial control cabinet interior featuring DIN rails, 3-phase MCB Q1, 24VDC power supply, PLC controller, terminal strip TB-01..12, and ground PE busbar).

### 📋 Inspection Checklists
- **File Extensions**: `.csv`, `.xlsx`, `.xls`.
- **Validation**:
  - File must contain at minimum the three required columns below.
  - Empty files or unparseable files are rejected with clear error messages.
  - Whitespace is automatically stripped from string values.

---

## 3. Checklist Column Schema Specification

### Required Columns (Baseline Schema)

| Column Header | Data Type | Description | Example |
|---|---|---|---|
| `check_id` | Text (Required) | Unique identifier for each checklist line item | `CHK-001` |
| `check_name` | Text (Required) | Descriptive title of the component or check | `Main Circuit Breaker (MCB)` |
| `expected_value` | Text (Required) | Engineering specification, presence, or label | `Present & ON` |

### Optional / Seeded Demo Columns

These optional columns enable pre-seeded demonstration records when real-time automated visual detection is not ready or when presenting deterministic demo scenarios to judges:

| Column Header | Data Type | Description | Supported Values / Example |
|---|---|---|---|
| `demo_found_value` | Text (Optional) | Observed state or finding in the cabinet | `Present & ON (Q1 63A)` |
| `demo_status` | Text (Optional) | Verification outcome status | `PASS`, `FAIL`, or `Needs Manual Check` (Unclear values default safely to `Needs Manual Check`) |
| `evidence_box` | Text (Optional) | Bounding box coordinates `x1,y1,x2,y2` | `"160,140,360,320"` |
| `component_type` | Text (Optional) | Functional category of component | `Circuit Breaker`, `Wiring`, `Terminal Block`, `Power Supply`, `Controller` |
| `notes` | Text (Optional) | Inspector notes or defect explanation | `Verified on top DIN rail [Sample Demo]` |

---

## 4. Included Sample Files

| File | Format | Purpose |
|---|---|---|
| [`sample_cabinet.png`](sample_cabinet.png) | PNG Image | Synthetic control cabinet photo with components mapped to the demo checklist. |
| [`sample_demo_checklist.csv`](sample_demo_checklist.csv) | CSV File | Pre-seeded demonstration checklist with PASS, FAIL, and Needs Manual Check items. |
| [`sample_demo_checklist.xlsx`](sample_demo_checklist.xlsx) | Excel File | Excel spreadsheet version of the demo checklist for testing `.xlsx` upload. |
| [`checklist_template.csv`](checklist_template.csv) | CSV File | Blank template for authoring custom inspection checklists. |

---

## 5. Judge Quick-Start Demonstration Instructions

1. Launch the application:
   ```bash
   streamlit run app.py
   ```
2. Click **🚀 Load Sample Demo Data** in the left sidebar to pre-populate both `sample_cabinet.png` and `sample_demo_checklist.csv`.
3. Alternatively, upload `sample_cabinet.png` in the photo uploader and `sample_demo_checklist.xlsx` in the checklist uploader to verify drag-and-drop file ingestion.
4. Click **🔍 Run Quality Inspection** to view the discrepancy table and annotated photograph.
5. In the Re-Inspection panel, click **🔧 Simulate Fix** to verify how corrected defects turn from FAIL to PASS.
