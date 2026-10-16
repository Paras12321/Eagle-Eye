# Sample Data Guidelines

This directory contains synthetic and sanitized sample data intended for testing and demonstration of the **EAGLE EYE** prototype.

## Privacy and Data Governance Policy

> [!IMPORTANT]
> **Never commit real proprietary data to this repository.**
> - Do **not** commit confidential industrial cabinet photographs.
> - Do **not** commit real client engineering CAD drawings (`.dwg`, `.dxf`, `.pdf`).
> - Do **not** commit actual production spreadsheets with proprietary part codes, serial numbers, or customer names.

All datasets stored in this folder must be synthetic, mock, or publicly approved templates.

## Included Files

- `checklist_template.csv`: A sample inspection checklist template demonstrating the required columns:
  - `check_id`: Unique identifier for each checklist line item (e.g. `CHK-001`).
  - `check_name`: Descriptive name of the item or component to inspect.
  - `expected_value`: Expected specification, state, or label marking.
  - `component_type`: Category of electrical component (Circuit Breaker, Terminal Block, Wiring, etc.).
  - `notes`: Additional inspection guidance or criteria.
