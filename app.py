"""EAGLE EYE — AI Vision for Cabinet Quality Control.

Interactive Hackathon Demonstration Application.
"""

import sys
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import streamlit as st

# Ensure project root and src/ are in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR / "src") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "src"))

from config.settings import (
    APP_TITLE,
    APP_TAGLINE,
    APP_VERSION,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_CHECKLIST_EXTENSIONS,
    DEFAULT_CHECKLIST_PATH,
    DEFAULT_DEMO_CHECKLIST_PATH,
    DEFAULT_SAMPLE_IMAGE_PATH,
)
from src.eagle_eye.input_processing.file_loader import (
    load_sample_demo_data,
    validate_image_file,
    validate_checklist_file,
    get_sample_image_path,
    get_sample_checklist_path,
)
from src.eagle_eye.vision.annotation import (
    draw_bounding_box,
    draw_issue_marker,
    draw_demo_evidence_label,
)
from src.eagle_eye.vision.image_processor import (
    save_annotated_image,
    save_evidence_crops,
)
from src.eagle_eye.inspection.result_models import (
    CheckStatus,
    InspectionSummary,
)
from src.eagle_eye.inspection.check_runner import (
    run_inspection,
)
from src.eagle_eye.reporting.report_generator import (
    generate_summary_dataframe,
    export_report_markdown,
)
from src.eagle_eye.reinspection.demo_recheck import (
    simulate_reinspection_fix,
)

# Page configuration
st.set_page_config(
    page_title="EAGLE EYE — Cabinet Quality Control",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for high-contrast inspection cards
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #0d6efd;
        margin-bottom: 12px;
    }
    .status-pass { color: #198754; font-weight: bold; }
    .status-fail { color: #dc3545; font-weight: bold; }
    .status-manual { color: #fd7e14; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header & Branding
st.title("🦅 EAGLE EYE")
st.subheader("AI Vision for Cabinet Quality Control")

# Prototype Honesty Banner
st.info(
    "🔬 **HACKATHON PROOF-OF-CONCEPT DEMONSTRATION**\n\n"
    "This prototype demonstrates an AI-assisted quality control workflow for industrial control cabinets. "
    "Automated findings are seeded from prepared verification samples and rule-based checks. "
    "**Eagle Eye never claims 100% accuracy**; ambiguous visual features are marked as "
    "**Needs Manual Check** for human inspector sign-off.",
    icon="ℹ️",
)

# Initialize Session State
if "cabinet_image" not in st.session_state:
    st.session_state["cabinet_image"] = None
if "image_name" not in st.session_state:
    st.session_state["image_name"] = None
if "checklist_df" not in st.session_state:
    st.session_state["checklist_df"] = None
if "checklist_name" not in st.session_state:
    st.session_state["checklist_name"] = None
if "inspection_summary" not in st.session_state:
    st.session_state["inspection_summary"] = None
if "reinspected" not in st.session_state:
    st.session_state["reinspected"] = False

# Sidebar: Controls & Sample Loading
with st.sidebar:
    st.header("⚡ Demo Quick Start")
    st.markdown(
        "If you do not have cabinet photos or checklists on hand, click below to load pre-configured sample data immediately:"
    )

    if st.button("🚀 Load Sample Demo Data", use_container_width=True, type="primary"):
        try:
            demo_img, demo_df = load_sample_demo_data()
            st.session_state["cabinet_image"] = demo_img
            st.session_state["image_name"] = "sample_cabinet.png (Pre-loaded Synthetic Demo)"
            st.session_state["checklist_df"] = demo_df
            st.session_state["checklist_name"] = "sample_demo_checklist.csv (Pre-loaded Seeded Demo)"
            st.session_state["inspection_summary"] = None
            st.session_state["reinspected"] = False
            st.success("✅ Sample demo image and checklist loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load sample demo: {e}")

    st.markdown("---")
    st.subheader("📁 Sample Assets Location")
    st.caption(
        "- **Cabinet Image**: `sample_data/sample_cabinet.png`\n"
        "- **Checklist CSV**: `sample_data/sample_demo_checklist.csv`\n"
        "- **Checklist Excel**: `sample_data/sample_demo_checklist.xlsx`\n"
        "- **Template**: `sample_data/checklist_template.csv`"
    )

    st.markdown("---")
    st.subheader("⚙️ System Status")
    st.caption(
        f"- **Version**: `{APP_VERSION}`\n"
        f"- **Image Formats**: `{', '.join(sorted(SUPPORTED_IMAGE_EXTENSIONS))}`\n"
        f"- **Checklist Formats**: `{', '.join(sorted(SUPPORTED_CHECKLIST_EXTENSIONS))}`\n"
        f"- **Privacy**: Sanitized synthetic data only (No proprietary photos)"
    )

    if st.button("🔄 Reset Demo State", use_container_width=True):
        st.session_state["cabinet_image"] = None
        st.session_state["image_name"] = None
        st.session_state["checklist_df"] = None
        st.session_state["checklist_name"] = None
        st.session_state["inspection_summary"] = None
        st.session_state["reinspected"] = False
        st.rerun()

st.markdown("---")

# Main Section 1: Inputs (Upload or Preloaded)
st.markdown("## 1️⃣ Input Intake: Photo & Checklist")

col_upload_left, col_upload_right = st.columns(2)

with col_upload_left:
    st.markdown("### 📷 Cabinet Photograph")
    uploaded_image_file = st.file_uploader(
        "Upload Cabinet Photo (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        key="image_uploader",
        help="Upload a frontal high-resolution photograph of the manufactured cabinet interior.",
    )

    if uploaded_image_file is not None:
        valid_img, err_img, decoded_img = validate_image_file(
            uploaded_image_file, filename=uploaded_image_file.name
        )
        if valid_img and decoded_img is not None:
            st.session_state["cabinet_image"] = decoded_img
            st.session_state["image_name"] = uploaded_image_file.name
            st.session_state["inspection_summary"] = None
            st.session_state["reinspected"] = False
            st.success(f"Loaded: `{uploaded_image_file.name}` ({decoded_img.shape[1]}x{decoded_img.shape[0]} px)")
        else:
            st.error(f"⚠️ Image Validation Error: {err_img}")

    if st.session_state["cabinet_image"] is not None:
        st.caption(f"Active image: **{st.session_state['image_name']}**")
        # Display thumbnail
        thumb_rgb = cv2.cvtColor(st.session_state["cabinet_image"], cv2.COLOR_BGR2RGB)
        st.image(thumb_rgb, caption="Cabinet Photo Preview", use_container_width=True)
    else:
        st.info("No cabinet photograph loaded yet. Upload an image above or click 'Load Sample Demo Data' in the sidebar.")

with col_upload_right:
    st.markdown("### 📋 Expected Engineering Checklist")
    uploaded_checklist_file = st.file_uploader(
        "Upload Checklist (CSV or Excel .xlsx)",
        type=["csv", "xlsx", "xls"],
        key="checklist_uploader",
        help="Upload component schedule with required columns: check_id, check_name, expected_value.",
    )

    if uploaded_checklist_file is not None:
        valid_chk, err_chk, parsed_df = validate_checklist_file(
            uploaded_checklist_file, filename=uploaded_checklist_file.name
        )
        if valid_chk and parsed_df is not None:
            st.session_state["checklist_df"] = parsed_df
            st.session_state["checklist_name"] = uploaded_checklist_file.name
            st.session_state["inspection_summary"] = None
            st.session_state["reinspected"] = False
            st.success(f"Loaded: `{uploaded_checklist_file.name}` ({len(parsed_df)} checks)")
        else:
            st.error(f"⚠️ Checklist Validation Error: {err_chk}")

    if st.session_state["checklist_df"] is not None:
        st.caption(f"Active checklist: **{st.session_state['checklist_name']}**")
        preview_cols = [c for c in ["check_id", "check_name", "expected_value", "demo_status"] if c in st.session_state["checklist_df"].columns]
        st.dataframe(st.session_state["checklist_df"][preview_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No checklist loaded yet. Upload a CSV/Excel file above or click 'Load Sample Demo Data' in the sidebar.")

st.markdown("---")

# Main Section 2: Trigger Inspection
st.markdown("## 2️⃣ Quality Inspection Execution")

ready_to_inspect = (
    st.session_state["cabinet_image"] is not None
    and st.session_state["checklist_df"] is not None
)

if not ready_to_inspect:
    st.warning("⚠️ Please provide both a Cabinet Photo and an Engineering Checklist before running inspection.")
else:
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run_clicked = st.button("🔍 Run Quality Inspection", type="primary", use_container_width=True)

    if run_clicked:
        with st.spinner("Analyzing cabinet photo and evaluating engineering checklist..."):
            summary = run_inspection(
                image=st.session_state["cabinet_image"],
                checklist_df=st.session_state["checklist_df"],
            )
            st.session_state["inspection_summary"] = summary
            st.session_state["reinspected"] = False

# Main Section 3: Inspection Outcomes & Visualizations
if st.session_state["inspection_summary"] is not None:
    summary: InspectionSummary = st.session_state["inspection_summary"]

    st.markdown("---")
    st.markdown("## 3️⃣ Inspection Results & Visual Discrepancy Evidence")

    if st.session_state["reinspected"]:
        st.success("🎉 **RE-INSPECTION UPDATED**: Simulated fix was verified and integrated into the report.")

    # High-level KPI Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Checks", summary.total_checks)
    kpi2.metric("✅ Passed", summary.passed_count)
    kpi3.metric("❌ Failed", summary.failed_count)
    kpi4.metric("🔍 Manual Check", summary.manual_check_count)
    overall_label = "PASS" if summary.is_overall_pass() else "ACTION REQUIRED"
    kpi5.metric("Overall Outcome", overall_label)

    # Detailed Checklist Results Table
    st.markdown("### 📊 Expected vs. Found Findings")
    summary_df = generate_summary_dataframe(summary)

    def color_status(val):
        if val == "PASS":
            return "background-color: #d1e7dd; color: #0f5132; font-weight: bold;"
        elif val == "FAIL":
            return "background-color: #f8d7da; color: #842029; font-weight: bold;"
        else:
            return "background-color: #fff3cd; color: #664d03; font-weight: bold;"

    styled_df = summary_df.style.map(color_status, subset=["Status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Visual Evidence & Annotated Image
    st.markdown("### 🔎 Physical Visual Evidence & Issue Markers")
    col_img_anno, col_legend = st.columns([3, 2])

    with col_img_anno:
        # Draw bounding boxes and numbered issue markers
        annotated_img = st.session_state["cabinet_image"].copy()
        markers_info = []

        for item in summary.items:
            if item.evidence_bbox is not None:
                # Color code: Green=PASS, Red=FAIL, Amber=MANUAL_CHECK
                if item.status == CheckStatus.PASS:
                    box_color = (0, 200, 0)
                elif item.status == CheckStatus.FAIL:
                    box_color = (0, 0, 220)
                else:
                    box_color = (0, 165, 255)

                label_text = f"{item.check_id}: {item.status.value}"
                annotated_img = draw_bounding_box(
                    annotated_img,
                    item.evidence_bbox,
                    label=label_text,
                    color=box_color,
                    thickness=3,
                )

                if item.marker_id is not None:
                    # Place circle marker at top-left of bbox
                    mx = max(20, item.evidence_bbox[0] + 16)
                    my = max(20, item.evidence_bbox[1] + 16)
                    marker_color = (0, 0, 220) if item.status == CheckStatus.FAIL else ((0, 165, 255) if item.status == CheckStatus.MANUAL_CHECK else (0, 180, 0))
                    annotated_img = draw_issue_marker(
                        annotated_img,
                        point=(mx, my),
                        marker_id=item.marker_id,
                        color=marker_color,
                        radius=14,
                    )
                    markers_info.append((item.marker_id, item.check_id, item.check_name, item.status.value, item.notes))

        # Stamp demo evidence watermark so judges know markers are seeded
        annotated_img = draw_demo_evidence_label(annotated_img)

        # Save annotated image to outputs/
        annotated_save_path = save_annotated_image(
            annotated_img,
            BASE_DIR / "outputs" / "annotated_cabinet.png",
        )

        # Save evidence crop snippets for FAIL items
        crop_paths = save_evidence_crops(
            st.session_state["cabinet_image"],
            summary.items,
            BASE_DIR / "outputs" / "evidence_crops",
        )

        annotated_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        st.image(
            annotated_rgb,
            caption="Cabinet Photograph Annotated with Numbered Quality Markers",
            use_container_width=True,
        )

    with col_legend:
        st.markdown("#### 🏷️ Quality Issue Markers Legend")
        if markers_info:
            for mid, cid, cname, stat, notes in markers_info:
                badge = "🔴 FAIL" if stat == "FAIL" else ("🟠 MANUAL CHECK" if stat == "Needs Manual Check" else "🟢 PASS")
                st.markdown(
                    f"- **Marker #{mid}** [{badge}] `{cid}` — **{cname}**\n"
                    f"  *{notes}*"
                )
        else:
            st.info("No localized visual bounding boxes specified for current items.")

        # Show evidence crops for FAIL items
        if crop_paths:
            st.markdown("#### 📸 FAIL Evidence Crops")
            for cid, cpath in crop_paths.items():
                crop_img = cv2.imread(cpath)
                if crop_img is not None:
                    crop_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                    st.image(crop_rgb, caption=f"Evidence crop: {cid} (sample/demo)", width=240)

    st.markdown("---")

    # Main Section 4: Export Reports & Simulated Re-inspection
    col_export, col_recheck = st.columns(2)

    with col_export:
        st.markdown("## 4️⃣ Export Inspection Report")
        st.markdown("Download auditable quality assurance records for factory compliance:")

        csv_data = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV Inspection Report",
            data=csv_data,
            file_name="eagle_eye_inspection_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

        md_report = export_report_markdown(summary)
        st.download_button(
            label="📝 Download Markdown Audit Summary",
            data=md_report.encode("utf-8"),
            file_name="eagle_eye_inspection_summary.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_recheck:
        st.markdown("## 5️⃣ Closed-Loop Re-Inspection")
        st.markdown(
            "Simulate a technician correcting a flagged discrepancy (e.g., securing the loose Safety Ground PE bonding wire) "
            "and re-verifying the cabinet:"
        )

        failing_items = [item for item in summary.items if item.status == CheckStatus.FAIL]

        if failing_items:
            target_item = failing_items[0]
            st.caption(f"Flagged Item for Fix: `{target_item.check_id}` — **{target_item.check_name}**")
            if st.button(f"🔧 Simulate Fix: Resolve {target_item.check_id} & Re-Inspect", type="secondary", use_container_width=True):
                updated_summary = simulate_reinspection_fix(
                    original_summary=summary,
                    target_check_id=target_item.check_id,
                    fixed_found_value=target_item.expected_value,
                    resolution_note="Field technician secured PE bonding lug to ground busbar with rated torque.",
                )
                st.session_state["inspection_summary"] = updated_summary
                st.session_state["reinspected"] = True
                st.rerun()
        else:
            st.success("✅ All failing checks resolved! No active failures pending re-inspection.")
