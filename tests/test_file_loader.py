"""Unit tests for file loading and validation.

Owned by: MEMBER 1 (Input Processing)
"""

from io import StringIO
import pytest
from src.eagle_eye.input_processing.file_loader import (
    is_valid_image_extension,
    is_valid_checklist_extension,
    load_checklist,
)
from config.settings import DEFAULT_CHECKLIST_PATH


def test_is_valid_image_extension():
    """Verify supported and unsupported image extensions."""
    assert is_valid_image_extension("cabinet.jpg") is True
    assert is_valid_image_extension("cabinet.JPEG") is True
    assert is_valid_image_extension("panel.png") is True
    assert is_valid_image_extension("drawing.pdf") is False
    assert is_valid_image_extension("document.txt") is False


def test_is_valid_checklist_extension():
    """Verify supported and unsupported checklist extensions."""
    assert is_valid_checklist_extension("checklist.csv") is True
    assert is_valid_checklist_extension("checklist.xlsx") is True
    assert is_valid_checklist_extension("notes.docx") is False


def test_load_checklist_from_template():
    """Verify that the default checklist template loads correctly."""
    assert DEFAULT_CHECKLIST_PATH.exists(), "Default checklist template must exist"
    df = load_checklist(DEFAULT_CHECKLIST_PATH)
    assert len(df) > 0
    assert "check_id" in df.columns
    assert "check_name" in df.columns
    assert "expected_value" in df.columns


def test_load_checklist_missing_columns():
    """Verify that a CSV missing required columns raises ValueError."""
    invalid_csv = StringIO("id,name\n1,breaker\n")
    with pytest.raises(ValueError, match="missing required column"):
        load_checklist(invalid_csv)
