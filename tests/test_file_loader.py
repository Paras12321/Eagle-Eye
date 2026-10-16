"""Unit tests for file loading and validation.

Owned by: MEMBER 1 (Input Processing)
"""

import io
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import pytest

from config.settings import (
    DEFAULT_CHECKLIST_PATH,
    DEFAULT_DEMO_CHECKLIST_PATH,
    DEFAULT_SAMPLE_IMAGE_PATH,
)
from src.eagle_eye.input_processing.file_loader import (
    is_valid_image_extension,
    is_valid_checklist_extension,
    parse_evidence_box,
    parse_demo_status,
    load_checklist,
    validate_checklist_file,
    load_cabinet_image,
    validate_image_file,
    load_sample_demo_data,
    checklist_to_inspection_results,
)
from src.eagle_eye.inspection.result_models import CheckStatus


def test_is_valid_image_extension():
    """Verify supported and unsupported image extensions."""
    assert is_valid_image_extension("cabinet.jpg") is True
    assert is_valid_image_extension("cabinet.JPEG") is True
    assert is_valid_image_extension("panel.png") is True
    assert is_valid_image_extension("drawing.pdf") is False
    assert is_valid_image_extension("document.txt") is False
    assert is_valid_image_extension("") is False
    assert is_valid_image_extension("cabinet.bmp") is False


def test_is_valid_checklist_extension():
    """Verify supported and unsupported checklist extensions."""
    assert is_valid_checklist_extension("checklist.csv") is True
    assert is_valid_checklist_extension("checklist.xlsx") is True
    assert is_valid_checklist_extension("checklist.XLS") is True
    assert is_valid_checklist_extension("notes.docx") is False
    assert is_valid_checklist_extension("data.json") is False
    assert is_valid_checklist_extension("") is False


def test_parse_evidence_box():
    """Verify parsing various evidence box string and sequence formats."""
    # Comma-separated string
    assert parse_evidence_box("160,140,360,320") == (160, 140, 360, 320)
    # Brackets and spaces
    assert parse_evidence_box("[160, 140, 360, 320]") == (160, 140, 360, 320)
    # Tuple or list
    assert parse_evidence_box([10, 20, 100, 200]) == (10, 20, 100, 200)
    # Invalid: inverted coordinates (x2 <= x1)
    assert parse_evidence_box("360,140,160,320") is None
    # Invalid: fewer than 4 values
    assert parse_evidence_box("100,200,300") is None
    # Invalid: non-numeric string
    assert parse_evidence_box("a,b,c,d") is None
    # Empty or None
    assert parse_evidence_box(None) is None
    assert parse_evidence_box("") is None


def test_parse_demo_status():
    """Verify that statuses are mapped accurately and safely default to MANUAL_CHECK."""
    assert parse_demo_status("PASS") == CheckStatus.PASS
    assert parse_demo_status("pass") == CheckStatus.PASS
    assert parse_demo_status("FAIL") == CheckStatus.FAIL
    assert parse_demo_status("fail") == CheckStatus.FAIL
    assert parse_demo_status("Needs Manual Check") == CheckStatus.MANUAL_CHECK
    assert parse_demo_status("MANUAL_CHECK") == CheckStatus.MANUAL_CHECK
    # Unclear or unknown strings default to MANUAL_CHECK (honest prototype requirement)
    assert parse_demo_status("unclear evidence") == CheckStatus.MANUAL_CHECK
    assert parse_demo_status(None) == CheckStatus.MANUAL_CHECK
    assert parse_demo_status("") == CheckStatus.MANUAL_CHECK


def test_load_checklist_from_template():
    """Verify that the default checklist template loads correctly."""
    assert DEFAULT_CHECKLIST_PATH.exists(), "Default checklist template must exist"
    df = load_checklist(DEFAULT_CHECKLIST_PATH)
    assert len(df) > 0
    assert "check_id" in df.columns
    assert "check_name" in df.columns
    assert "expected_value" in df.columns


def test_load_checklist_from_demo_csv():
    """Verify that the demo checklist with seeded records loads accurately."""
    assert DEFAULT_DEMO_CHECKLIST_PATH.exists(), "Demo checklist file must exist"
    df = load_checklist(DEFAULT_DEMO_CHECKLIST_PATH)
    assert len(df) >= 3
    assert "demo_status" in df.columns
    assert "evidence_box" in df.columns


def test_load_checklist_from_excel():
    """Verify loading from an Excel file buffer."""
    excel_path = DEFAULT_DEMO_CHECKLIST_PATH.with_suffix(".xlsx")
    if excel_path.exists():
        df = load_checklist(excel_path)
        assert len(df) > 0
        assert "check_id" in df.columns


def test_load_checklist_missing_columns():
    """Verify that a CSV missing required columns raises ValueError."""
    invalid_csv = io.StringIO("id,name\n1,breaker\n")
    with pytest.raises(ValueError, match="missing required column"):
        load_checklist(invalid_csv)


def test_load_checklist_empty_file():
    """Verify that an empty file raises ValueError."""
    empty_csv = io.StringIO("")
    with pytest.raises(ValueError):
        load_checklist(empty_csv)


def test_load_checklist_unsupported_format(tmp_path):
    """Verify that an unsupported file format raises ValueError."""
    dummy_txt = tmp_path / "checklist.txt"
    dummy_txt.write_text("CHK-1,MCB,Present")
    with pytest.raises(ValueError, match="Unsupported checklist format"):
        load_checklist(dummy_txt)


def test_validate_checklist_file_valid():
    """Verify that validate_checklist_file returns success for valid content."""
    valid_csv = io.StringIO("check_id,check_name,expected_value\nCHK-01,Relay,ON\n")
    valid, err, df = validate_checklist_file(valid_csv, filename="checks.csv")
    assert valid is True
    assert err is None
    assert df is not None
    assert len(df) == 1


def test_validate_checklist_file_invalid():
    """Verify that validate_checklist_file returns friendly error for invalid extension."""
    valid, err, df = validate_checklist_file("sample.pdf", filename="sample.pdf")
    assert valid is False
    assert "Invalid file format" in err
    assert df is None


def test_load_cabinet_image_from_path():
    """Verify loading the synthetic sample cabinet image from disk."""
    assert DEFAULT_SAMPLE_IMAGE_PATH.exists(), "Sample cabinet image must exist"
    img = load_cabinet_image(DEFAULT_SAMPLE_IMAGE_PATH)
    assert isinstance(img, np.ndarray)
    assert img.ndim == 3
    assert img.shape[0] > 0 and img.shape[1] > 0


def test_load_cabinet_image_from_bytes():
    """Verify decoding an image from raw PNG/JPG bytes."""
    # Create small valid test image in memory
    synthetic = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(synthetic, (10, 10), (90, 90), (0, 255, 0), -1)
    _, encoded = cv2.imencode(".png", synthetic)
    raw_bytes = encoded.tobytes()

    img = load_cabinet_image(raw_bytes, filename="test.png")
    assert img.shape == (100, 100, 3)


def test_load_cabinet_image_invalid_bytes():
    """Verify that corrupt bytes raise ValueError."""
    corrupt_bytes = b"NOT_A_VALID_IMAGE_DATA_12345"
    with pytest.raises(ValueError, match="Failed to decode cabinet image"):
        load_cabinet_image(corrupt_bytes, filename="corrupt.png")


def test_validate_image_file_invalid_ext():
    """Verify that validate_image_file catches invalid extensions."""
    valid, err, img = validate_image_file(b"data", filename="drawing.pdf")
    assert valid is False
    assert "Invalid image format" in err
    assert img is None


def test_load_sample_demo_data():
    """Verify that load_sample_demo_data loads both sample image and checklist."""
    img, df = load_sample_demo_data()
    assert isinstance(img, np.ndarray)
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 3


def test_checklist_to_inspection_results():
    """Verify conversion of demo checklist into InspectionItemResult list."""
    df = pd.DataFrame([
        {
            "check_id": "CHK-01",
            "check_name": "Breaker",
            "expected_value": "Present",
            "demo_found_value": "Present",
            "demo_status": "PASS",
            "evidence_box": "100,100,200,200",
            "notes": "Verified",
        },
        {
            "check_id": "CHK-02",
            "check_name": "PE Ground",
            "expected_value": "Connected",
            "demo_found_value": "Disconnected",
            "demo_status": "FAIL",
            "evidence_box": "300,300,400,400",
            "notes": "Loose wire",
        },
    ])
    items = checklist_to_inspection_results(df)
    assert len(items) == 2
    assert items[0].status == CheckStatus.PASS
    assert items[0].evidence_bbox == (100, 100, 200, 200)
    assert items[0].marker_id == 1

    assert items[1].status == CheckStatus.FAIL
    assert items[1].evidence_bbox == (300, 300, 400, 400)
    assert items[1].marker_id == 2
