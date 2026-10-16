"""EAGLE EYE — AI Vision for Cabinet Quality Control.

Minimal Streamlit starter application.
"""

import sys
from pathlib import Path
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
    DEFAULT_CHECKLIST_PATH,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_CHECKLIST_EXTENSIONS,
)

# Page configuration
st.set_page_config(
    page_title="EAGLE EYE — Cabinet Quality Control",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Header & Branding
st.title("🦅 EAGLE EYE")
st.subheader("AI Vision for Cabinet Quality Control")

# Visible Prototype / Under Development Banner
st.warning(
    f"🛠️ **PROTOTYPE FOUNDATION — UNDER DEVELOPMENT** (Version: `{APP_VERSION}`)\n\n"
    "This initial environment establishes the project structure, configuration, and interfaces. "
    "Automated computer vision checks and checklist comparisons will be implemented "
    "in subsequent development tasks.",
    icon="⚠️",
)

st.markdown("---")

# Overview Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Project Overview")
    st.markdown(
        f"**{APP_TAGLINE}**\n\n"
        "Industrial electrical control cabinets house critical breakers, controllers, terminal "
        "blocks, and wiring harness assemblies. During manual manufacturing inspection, verifying "
        "every single component and label against engineering drawings is labor-intensive and "
        "susceptible to human oversight.\n\n"
        "**EAGLE EYE** is designed to assist quality control inspectors by pairing an uploaded cabinet "
        "photograph with an expected component checklist to run automated verification checks, "
        "highlight discrepancies, and generate auditable inspection reports."
    )

    st.markdown("### 🔄 Planned Demonstration Workflow")
    workflow_steps = [
        "1️⃣ **Upload Cabinet Photo**: Inspector uploads a high-resolution cabinet photograph (JPG / PNG).",
        "2️⃣ **Upload Expected Checklist**: Upload engineering checklist specifications (CSV / Excel).",
        "3️⃣ **Run Quality Inspection**: Trigger automated verification checks against expected values.",
        "4️⃣ **Display Check Results**: Review structured outcomes (**PASS**, **FAIL**, or **Needs Manual Check**).",
        "5️⃣ **Expected vs. Found Comparison**: Inspect side-by-side component discrepancy tables.",
        "6️⃣ **Visual Evidence & Annotations**: View photograph annotated with numbered issue markers.",
        "7️⃣ **Download Inspection Report**: Export audit-ready CSV or Markdown quality reports.",
        "8️⃣ **Simulated Re-Inspection**: Validate a fix and confirm updated pass status.",
    ]
    for step in workflow_steps:
        st.markdown(f"- {step}")

with col_right:
    st.markdown("### ⚙️ System Status")
    st.info(
        f"- **Python Version**: `{sys.version.split()[0]}`\n"
        f"- **Environment**: `Development`\n"
        f"- **Supported Images**: `{', '.join(sorted(SUPPORTED_IMAGE_EXTENSIONS))}`\n"
        f"- **Supported Checklists**: `{', '.join(sorted(SUPPORTED_CHECKLIST_EXTENSIONS))}`\n"
        f"- **Sample Template**: `{'Found' if DEFAULT_CHECKLIST_PATH.exists() else 'Missing'}`"
    )

    st.markdown("### 👥 Team Ownership")
    st.markdown(
        "- **Member 1**: Input Processing & Data Validation\n"
        "- **Member 2**: Computer Vision & Annotations\n"
        "- **Member 3**: Inspection Rules & Result Models\n"
        "- **Member 4**: UI, Reporting & Integration"
    )

st.markdown("---")

# Input Preview Placeholder (Explicitly non-functional placeholder)
st.markdown("### 🚀 Module Staging")
st.info(
    "💡 **Next Steps**: Active development begins with Module 1 (Input Processing: Image and Checklist upload) "
    "and Module 2 (Vision: OpenCV rendering & issue markers). Connect your local virtual environment "
    "and run `pytest -q` to verify starter components."
)
