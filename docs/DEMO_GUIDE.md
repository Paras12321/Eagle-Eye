# EAGLE EYE — Hackathon Demonstration Guide

This guide outlines the planned 8-step live demonstration workflow for hackathon judges and evaluators once feature modules are integrated.

---

## Planned Demonstration Narrative

| Step | Action in Streamlit UI | Judge / Evaluator Talking Point |
|---|---|---|
| **Step 1** | Upload cabinet photo (`sample_data/` synthetic image) | *"Inspectors begin by uploading a standard high-resolution photograph of the manufactured control cabinet."* |
| **Step 2** | Upload or select expected checklist | *"The engineering specifications and component requirements are loaded directly from a CSV or Excel schedule."* |
| **Step 3** | Click **Run Inspection** | *"EAGLE EYE's verification engine compares the physical photo against required checklist values."* |
| **Step 4** | Review Overview KPI Cards | *"The inspector immediately sees a high-level summary: Total Checks, Passed, Failed, and items needing Manual Review."* |
| **Step 5** | Examine Expected vs. Found Table | *"A granular discrepancy table reveals what was expected (e.g. 3-pole breaker Q1) versus what was verified."* |
| **Step 6** | View Annotated Photograph | *"Numbered visual markers pinpoint exactly where a defect or issue was identified on the physical cabinet."* |
| **Step 7** | Export Inspection Report | *"With one click, an audit-ready CSV or Markdown quality report is exported for factory quality records."* |
| **Step 8** | Demonstrate Re-Inspection | *"Simulates a technician replacing a missing part, re-running the check to confirm the status turns green (PASS)."* |

---

## Demonstration Tips & Preparation

1. **Pre-test the Environment**: Ensure the Python environment is activated and `streamlit run app.py` launches cleanly before presentation time.
2. **Use Sanitized Data**: Always present using synthetic demo data from `sample_data/`.
3. **Be Transparent About Prototype Scope**: Highlight that this prototype is a modular proof-of-concept demonstrating AI-assisted visual workflow, not an exhaustive production computer vision system.
