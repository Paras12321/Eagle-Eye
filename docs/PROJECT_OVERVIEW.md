# EAGLE EYE — Project Overview

## 1. Executive Summary

**EAGLE EYE** is an AI-assisted quality inspection prototype engineered for electrical control cabinet manufacturing and factory acceptance testing (FAT). By pairing high-resolution photographs of control cabinets with digitized engineering checklists, EAGLE EYE aims to automate routine visual checks, identify missing or misplaced components, flag labeling discrepancies, and generate audit-ready inspection reports.

## 2. Problem Statement

Electrical control cabinets are critical power distribution and industrial automation assemblies containing circuit breakers, motor starters, PLCs, relays, terminal rails, and dense wiring harnesses. 

During manual quality control:
- **High Cognitive Load**: Human inspectors must cross-reference complex engineering schematics and bill-of-materials against hundreds of tightly packed components.
- **Error Vulnerability**: Minor discrepancies—such as an unseated DIN rail terminal, incorrect breaker amp rating, or unlabeled ground wire—can escape visual inspection, leading to hazardous field failures, factory downtime, or expensive rework.
- **Lack of Digital Audit Trails**: Many inspection processes rely on physical paper checklists or manual spreadsheet entries without photographic proof linked to specific checklist items.

## 3. Proposed Solution

EAGLE EYE introduces a lightweight, modular software prototype demonstrating how computer vision and automated checklist rules can assist quality inspectors:

1. **Digital Intake**: Ingests high-resolution cabinet photographs along with engineering specifications (CSV/Excel).
2. **Rule-Based & Visual Verification**: Evaluates component presence, sequential terminal labeling, and key safety features against expected values.
3. **Evidence-Backed Results**: Marks photographic evidence with numbered visual indicators corresponding directly to flagged checklist items.
4. **Audit Reporting**: Exports structured inspection reports (CSV and Markdown) with itemized PASS, FAIL, and Needs Manual Check determinations.
5. **Simulated Closed-Loop Re-Inspection**: Demonstrates how corrected defects are verified and cleared during follow-up inspection.

## 4. Planned 8-Step Demonstration Workflow

```text
[1. Upload Cabinet Image] (JPG/PNG)
             │
             ▼
[2. Upload Expected Checklist] (CSV/Excel)
             │
             ▼
[3. Run Automated Checks] (Rule-based & Vision inspection)
             │
             ▼
[4. Display Status Summaries] (PASS / FAIL / Needs Manual Check)
             │
             ▼
[5. Expected vs. Found Table] (Component-by-component comparison)
             │
             ▼
[6. Visual Evidence Overlay] (Numbered markers on cabinet photo)
             │
             ▼
[7. Download Inspection Report] (CSV / Markdown exports)
             │
             ▼
[8. Simulated Re-Inspection] (Verify simulated fix & status update)
```

## 5. Scope & Boundary Conditions

> [!NOTE]
> This project is a **hackathon proof-of-concept prototype**.
> It focuses on delivering a functional end-to-end demonstration workflow. It deliberately avoids heavy production infrastructure, custom neural network training pipelines, external cloud API dependencies, and complex distributed microservices.
