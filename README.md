# EAGLE EYE

> **AI Vision for Cabinet Quality Control**  
> *A modular, AI-assisted quality inspection prototype for electrical control cabinets.*

---

## 1. Project Title & Tagline
**EAGLE EYE — AI Vision for Cabinet Quality Control**  
*Empowering manufacturing quality inspectors with automated checklist verification, visual discrepancy detection, and audit reporting for electrical control cabinets.*

---

## 2. Project Overview
**EAGLE EYE** is a lightweight, Python-based quality inspection prototype developed for industrial control cabinet manufacturing and factory acceptance testing (FAT). In electrical assembly facilities, engineers and technicians assemble complex panels containing circuit breakers, terminal rails, PLCs, safety relays, and dense wiring harnesses. 

EAGLE EYE assists inspectors by pairing a single high-resolution photograph of a manufactured control cabinet with a structured engineering checklist (CSV or Excel). It runs automated verification rules, visualizes flagged issues directly on the photograph with numbered markers, and produces an exportable audit report.

---

## 3. Problem Statement
Industrial control cabinet inspection currently faces several operational challenges:
- **Labor-Intensive Manual Review**: Verifying hundreds of components and terminal labels against engineering schematics is slow and mentally exhausting.
- **Human Oversight Risk**: Minor discrepancies—such as an omitted circuit breaker, inverted wire color, or missing terminal marker—can easily be missed during long shifts.
- **Costly Field Rework**: Defects discovered after shipment or during commissioning cause costly delays, hazardous safety violations, and warranty expenses.
- **Incomplete Audit Trails**: Paper-based inspection notes often lack photographic evidence tied directly to specific line items.

---

## 4. Proposed Solution
EAGLE EYE addresses these challenges by providing a simple, human-in-the-loop digital inspection assistant:
- Ingests standard cabinet photographs and checklist files.
- Evaluates components against expected engineering values using rule-based checks.
- Generates transparent statuses: **PASS**, **FAIL**, or **Needs Manual Check**.
- Annotates the physical cabinet photo with numbered visual issue markers and bounding boxes.
- Exports structured inspection reports (CSV and Markdown) for audit compliance.
- Demonstrates a closed-loop re-inspection workflow where corrected defects are verified.

---

## 5. How the Prototype is Expected to Work
The planned workflow consists of an intuitive 8-step process:
1. **Upload Cabinet Photo**: The inspector uploads a standard photograph (`.jpg`, `.jpeg`, `.png`) of the cabinet interior.
2. **Upload Expected Checklist**: The inspector uploads an engineering checklist (`.csv`, `.xlsx`) specifying required components, labels, and ratings.
3. **Run Quality Inspection**: The inspector clicks *Run Inspection* to execute automated verification rules.
4. **Display Summary Results**: High-level KPI cards show overall status along with total passed, failed, and flagged checks.
5. **Expected vs. Found Comparison**: A side-by-side discrepancy table highlights exact differences between expected values and detected states.
6. **Visual Evidence & Annotations**: An annotated cabinet image displays bounding boxes and numbered issue markers corresponding to flagged checklist rows.
7. **Download Inspection Report**: The user downloads an audit-ready CSV or Markdown quality report.
8. **Demonstrate Re-Inspection**: The inspector triggers a simulated fix to observe the status turn from FAIL to PASS.

---

## 6. Planned Features
- [ ] Drag-and-drop file upload for JPG/PNG images and CSV/Excel checklists.
- [ ] Automated format and column validation with descriptive error guidance.
- [ ] Rule-based expected-versus-found evaluation logic.
- [ ] Numbered visual marker rendering and evidence cropping using OpenCV.
- [ ] High-contrast Streamlit dashboard with KPI metric cards and result tables.
- [ ] Audit report export to CSV and formatted Markdown.
- [ ] Simulated re-inspection demonstration for hackathon presentation.

---

## 7. Technology Stack
EAGLE EYE uses a lean, accessible Python technology stack without heavy microservices or cloud dependencies:
- **Language**: Python 3.10+
- **User Interface**: [Streamlit](https://streamlit.io/) (for rapid interactive dashboards)
- **Computer Vision & Drawing**: [OpenCV](https://opencv.org/) (`opencv-python` for image manipulation and annotation)
- **Data Handling**: [pandas](https://pandas.pydata.org/) (for checklist parsing and tabular results)
- **Spreadsheet Support**: [openpyxl](https://openpyxl.readthedocs.io/) (for reading Excel `.xlsx` checklists)
- **Testing**: [pytest](https://pytest.org/) (for unit testing and interface validation)

---

## 8. Project Folder Structure

```text
Eagle-Eye/
│
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git exclusion rules
├── .env.example                        # Environment variables template
│
├── app.py                              # Streamlit web application starter
│
├── config/
│   ├── __init__.py
│   └── settings.py                     # Global paths and application settings
│
├── src/
│   └── eagle_eye/
│       ├── __init__.py                 # Package metadata
│       │
│       ├── input_processing/           # Owned by Member 1
│       │   ├── __init__.py
│       │   └── file_loader.py          # File intake and validation
│       │
│       ├── vision/                     # Owned by Member 2
│       │   ├── __init__.py
│       │   ├── image_processor.py      # Image decoding & resizing
│       │   └── annotation.py           # Bounding boxes & issue markers
│       │
│       ├── inspection/                 # Owned by Member 3
│       │   ├── __init__.py
│       │   ├── check_runner.py         # Inspection execution runner
│       │   └── result_models.py        # Data models & CheckStatus enum
│       │
│       ├── reporting/                  # Owned by Member 4
│       │   ├── __init__.py
│       │   └── report_generator.py     # CSV and Markdown report generation
│       │
│       └── reinspection/               # Owned by Member 4
│           ├── __init__.py
│           └── demo_recheck.py         # Simulated fix verification
│
├── tests/
│   ├── __init__.py
│   ├── test_file_loader.py             # Input validation tests
│   ├── test_check_runner.py            # Inspection model tests
│   └── test_annotation.py              # Visual annotation tests
│
├── sample_data/
│   ├── README.md                       # Sample data usage and privacy notice
│   └── checklist_template.csv          # Starter checklist template
│
├── outputs/
│   └── .gitkeep                        # Output directory for exported reports
│
├── docs/
│   ├── PROJECT_OVERVIEW.md             # Detailed domain background
│   ├── ARCHITECTURE.md                 # System flow and package design
│   ├── TEAM_RESPONSIBILITIES.md        # Four-member team allocation
│   ├── DEMO_GUIDE.md                   # 8-step presentation walkthrough
│   └── KNOWN_LIMITATIONS.md            # Out-of-scope research gaps
│
└── scripts/
    └── run_tests.py                    # Cross-platform test execution script
```

---

## 9. Explanation of Important Modules

- **`config/settings.py`**: Centralizes file paths, accepted file extensions, and application constants to avoid hardcoded values.
- **`src/eagle_eye/input_processing/file_loader.py`**: Validates file types and safely parses checklist data into standardized pandas DataFrames.
- **`src/eagle_eye/vision/image_processor.py`**: Handles OpenCV byte decoding, image scaling, and sub-image evidence cropping.
- **`src/eagle_eye/vision/annotation.py`**: Renders clear bounding boxes and circular numbered issue markers on cabinet images.
- **`src/eagle_eye/inspection/result_models.py`**: Defines the single source of truth for result structures (`CheckStatus`, `InspectionItemResult`, `InspectionSummary`).
- **`src/eagle_eye/inspection/check_runner.py`**: Orchestrates checklist evaluations against image features.
- **`src/eagle_eye/reporting/report_generator.py`**: Exports structured summaries into displayable DataFrames, CSV files, and Markdown tables.
- **`src/eagle_eye/reinspection/demo_recheck.py`**: Simulates fixing an identified flaw to showcase the closed-loop workflow during demonstrations.

---

## 10. Installation Prerequisites
Before running EAGLE EYE, ensure your system has:
- **Python 3.10, 3.11, 3.12, or 3.13** installed.
- **Git** installed and configured.
- A modern web browser (Chrome, Edge, Firefox, or Safari).

---

## 11. Virtual Environment Setup for Windows
Open **PowerShell** in the project root:

```powershell
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1
```

*(Note: If PowerShell execution policy restricts scripts, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in the current session).*

---

## 12. Virtual Environment Setup for Linux/macOS
Open a terminal in the project root:

```bash
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

---

## 13. Dependency Installation Instructions
With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

---

## 14. How to Launch the Streamlit Application
Launch the web interface locally:

```bash
streamlit run app.py
```

The Streamlit server will start and open your browser automatically at `http://localhost:8501`.

---

## 15. How to Run Tests
Run the test suite using pytest:

```bash
pytest -q
```

Alternatively, execute the cross-platform test script:

```bash
python scripts/run_tests.py
```

---

## 16. Expected Checklist File Format
Inspection checklists can be provided as **CSV** or **Excel (`.xlsx`)** files. The checklist must include at minimum the following columns:

| Column Header | Type | Description | Example |
|---|---|---|---|
| `check_id` | Text | Unique identifier for the inspection rule | `CHK-001` |
| `check_name` | Text | Descriptive name of the item or component | `Main Circuit Breaker (MCB)` |
| `expected_value` | Text | Required specification, presence, or label | `Present` |

Optional columns such as `component_type` and `notes` are supported and displayed when present. A starter template is provided at [`sample_data/checklist_template.csv`](sample_data/checklist_template.csv).

---

## 17. Sample Demonstration Instructions
1. Activate your virtual environment and launch `streamlit run app.py`.
2. Inspect the **System Status** panel to verify that the environment and sample checklist template are detected.
3. Review the planned 8-step workflow on the homepage.
4. Run `pytest -q` to confirm all 11 baseline unit tests pass.

---

## 18. Four-Member Team Responsibilities
- **Member 1 (Input Processing)**: Image and checklist upload, file validation, format error handling (`src/eagle_eye/input_processing/`).
- **Member 2 (Computer Vision)**: Image loading, aspect ratio scaling, bounding boxes, numbered markers, evidence cropping (`src/eagle_eye/vision/`).
- **Member 3 (Inspection Logic)**: Result data models, rule-based comparison engine, PASS/FAIL/Manual Check determination (`src/eagle_eye/inspection/`).
- **Member 4 (UI, Reporting & Integration)**: Streamlit interface, workflow orchestration, CSV/Markdown reporting, simulated re-inspection (`app.py`, `src/eagle_eye/reporting/`, `src/eagle_eye/reinspection/`).

Detailed team protocols and shared interface guidelines are documented in [`docs/TEAM_RESPONSIBILITIES.md`](docs/TEAM_RESPONSIBILITIES.md).

---

## 19. Current Implementation Status

> [!IMPORTANT]
> **Foundation & Architecture Initialized.**  
> This task initializes the complete project structure, data contracts, environment configuration, starter tests, and documentation. The core automated computer vision detection rules and interactive checklist evaluation features will be implemented module-by-module in subsequent development tasks.

---

## 20. Known Limitations
- Evaluates a single frontal 2D photograph per inspection; multi-camera stereo fusion is not supported.
- Inspection rules are rule-based prototypes, not fine-tuned commercial deep neural networks.
- Designed as a local, offline proof-of-concept; cloud deployment and enterprise databases are omitted.
- Out-of-scope research gaps (statistical fault benchmarking, synthetic fault generation, full CAD alignment) are intentionally excluded. See [`docs/KNOWN_LIMITATIONS.md`](docs/KNOWN_LIMITATIONS.md).

---

## 21. Future Enhancements
- Integration of lightweight on-device OCR (e.g. Tesseract or EasyOCR) for automated wire ferrule and terminal strip label reading.
- Support for multiple camera perspectives (enclosure door, sub-panel, wire ducts).
- PDF inspection report generation with embedded thumbnail crops.
- Real-time video stream inspection from an industrial inspection camera or tablet.

---

## 22. Privacy and Data-Handling Rules
To protect industrial intellectual property and confidential customer data:
- **Never commit `.env` files, API credentials, or passwords.**
- **Never commit proprietary cabinet photographs, client CAD schematics (`.dwg`, `.dxf`), or confidential production checklists.**
- All sample files committed to version control must be synthetic or sanitized templates located in [`sample_data/`](sample_data/).
- The `.gitignore` file enforces exclusions for private assets and generated outputs.

---

## 23. Disclaimer
This software is an experimental prototype developed solely for educational and hackathon demonstration purposes. It is not certified for industrial safety-critical validation or regulatory compliance. Any production deployment requires thorough domain-specific validation and human engineering oversight.
