# EAGLE EYE — Known Limitations & Research Boundaries

To ensure focus and feasibility within a fast-paced hackathon setting, the scope of EAGLE EYE is strictly defined around a workable interactive demonstration.

---

## 1. Explicitly Out-of-Scope Research Gaps

The following capabilities represent advanced academic or industrial research challenges and are **deliberately excluded** from the prototype scope:

- **Formal Research-Gap Experiments**: Academic benchmark comparisons against external computer vision baselines.
- **Fault-Level Statistical Metrics**: Formal calculation of fault-level Precision, Recall, F1 scores, or confusion matrices across exhaustive error taxonomies.
- **Camera Robustness Testing**: Extensive invariance experiments across extreme lighting conditions, lens distortion, acute glare, motion blur, and non-perpendicular camera angles.
- **Synthetic Fault Generation Framework**: Generative AI or diffusion-based pipelines to synthetically inject physical cabinet flaws into clean photos.
- **Custom Model Training**: Training custom deep neural networks or fine-tuning vision transformers from scratch on proprietary datasets.
- **Full Drawing-to-Photo Spatial Alignment**: Automated 2D-to-3D registration between CAD vector schematics and perspective photographs.
- **Sub-Millimeter Wire & Ferrule Tracing**: Complete physical wire continuity tracing, terminal torque inspection, or microscopic ferrule crimp verification.
- **Enterprise Lifecycle Management**: Multi-user role-based access control (RBAC), cloud databases, microservices architecture, and ERP integration.

---

## 2. Current Prototype Operational Constraints

- **Single Photo Analysis**: The initial workflow evaluates a single, frontal cabinet photograph per run rather than multi-angle stereo feeds.
- **Offline / Local Execution**: The application runs entirely on the inspector's local workstation without requiring internet access or cloud services.
- **Human-in-the-Loop Philosophy**: Flagged discrepancies and items marked as `Needs Manual Check` are intended to alert and empower the human inspector, not replace human judgment.
- **Standardized Checklist Input**: Requires structured CSV or Excel input matching the template specifications.
