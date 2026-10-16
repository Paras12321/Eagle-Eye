"""Global configuration and project paths for Eagle Eye."""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
OUTPUTS_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"

# Application metadata
APP_TITLE = "EAGLE EYE — AI Vision for Cabinet Quality Control"
APP_TAGLINE = "AI-assisted quality inspection prototype for electrical control cabinets"
APP_VERSION = "0.1.0-alpha (Foundation)"

# Supported file formats
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
SUPPORTED_CHECKLIST_EXTENSIONS = {".csv", ".xlsx"}

# Default files
DEFAULT_CHECKLIST_PATH = SAMPLE_DATA_DIR / "checklist_template.csv"

# Minimum required columns in the checklist
REQUIRED_CHECKLIST_COLUMNS = ["check_id", "check_name", "expected_value"]
