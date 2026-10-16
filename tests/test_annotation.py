"""Unit tests for visual annotations and image processing.

Owned by: MEMBER 2 (Computer Vision)
"""

import numpy as np
import cv2
from pathlib import Path
from src.eagle_eye.vision.annotation import draw_bounding_box, draw_issue_marker, draw_demo_evidence_label
from src.eagle_eye.vision.image_processor import (
    resize_image_aspect_ratio,
    extract_crop,
    load_image_from_bytes,
    save_annotated_image,
    save_evidence_crops,
    try_ocr_region,
)


def test_draw_bounding_box():
    """Verify that draw_bounding_box draws on an image without altering dimensions."""
    canvas = np.zeros((200, 200, 3), dtype=np.uint8)
    annotated = draw_bounding_box(canvas, (10, 10, 80, 80), label="Breaker")

    assert annotated.shape == canvas.shape
    assert np.any(annotated > 0), "Annotated image should contain non-zero pixel values"


def test_draw_issue_marker():
    """Verify that draw_issue_marker creates a visible marker."""
    canvas = np.zeros((200, 200, 3), dtype=np.uint8)
    annotated = draw_issue_marker(canvas, (100, 100), marker_id=1)

    assert annotated.shape == canvas.shape
    assert np.any(annotated > 0)


def test_resize_aspect_ratio():
    """Verify aspect ratio resizing logic."""
    canvas = np.zeros((1000, 2000, 3), dtype=np.uint8)
    resized, scale = resize_image_aspect_ratio(canvas, max_dim=1000)

    assert resized.shape[1] == 1000  # width scaled to max_dim
    assert resized.shape[0] == 500   # height scaled proportionally
    assert scale == 0.5


def test_extract_crop():
    """Verify crop extraction from bounding box."""
    canvas = np.ones((100, 100, 3), dtype=np.uint8) * 50
    crop = extract_crop(canvas, (10, 20, 30, 60))

    assert crop.shape == (40, 20, 3)


# ---------------------------------------------------------------------------
#  New tests added by Member 2
# ---------------------------------------------------------------------------


def test_draw_demo_evidence_label():
    """Verify that draw_demo_evidence_label adds visible watermark pixels."""
    canvas = np.zeros((200, 400, 3), dtype=np.uint8)
    result = draw_demo_evidence_label(canvas)

    assert result.shape == canvas.shape
    # The bottom banner region should now have non-zero pixels
    bottom_strip = result[-20:, :, :]
    assert np.any(bottom_strip > 0), "Watermark banner should render visible pixels"


def test_save_annotated_image(tmp_path):
    """Verify that save_annotated_image writes a valid PNG file to disk."""
    canvas = np.ones((100, 200, 3), dtype=np.uint8) * 128
    annotated = draw_bounding_box(canvas, (10, 10, 90, 90), label="Test")
    out_path = tmp_path / "annotated_test.png"

    saved_path = save_annotated_image(annotated, out_path)
    assert Path(saved_path).exists(), "Annotated image file should exist on disk"
    assert Path(saved_path).stat().st_size > 0, "Saved file should not be empty"

    # Verify the saved file can be decoded back
    reloaded = cv2.imread(saved_path)
    assert reloaded is not None
    assert reloaded.shape == annotated.shape


def test_save_annotated_image_rejects_empty():
    """Verify that save_annotated_image raises ValueError for empty images."""
    empty = np.array([], dtype=np.uint8)
    try:
        save_annotated_image(empty, "should_not_exist.png")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_save_evidence_crops(tmp_path):
    """Verify that save_evidence_crops extracts and saves FAIL item crops."""
    from src.eagle_eye.inspection.result_models import InspectionItemResult, CheckStatus

    canvas = np.ones((200, 300, 3), dtype=np.uint8) * 100

    items = [
        InspectionItemResult(
            check_id="CHK-F1",
            check_name="Failing Item",
            expected_value="OK",
            found_value="Bad",
            status=CheckStatus.FAIL,
            evidence_bbox=(10, 10, 50, 50),
        ),
        InspectionItemResult(
            check_id="CHK-P1",
            check_name="Passing Item",
            expected_value="OK",
            found_value="OK",
            status=CheckStatus.PASS,
            evidence_bbox=(60, 60, 100, 100),
        ),
        InspectionItemResult(
            check_id="CHK-F2-NOBBOX",
            check_name="Fail No BBox",
            expected_value="OK",
            found_value="Bad",
            status=CheckStatus.FAIL,
            evidence_bbox=None,
        ),
    ]

    crop_dir = tmp_path / "crops"
    saved = save_evidence_crops(canvas, items, crop_dir)

    # Only CHK-F1 should be saved (FAIL + has bbox). CHK-P1 is PASS, CHK-F2-NOBBOX has no bbox.
    assert "CHK-F1" in saved
    assert "CHK-P1" not in saved
    assert "CHK-F2-NOBBOX" not in saved
    assert Path(saved["CHK-F1"]).exists()


def test_try_ocr_region_graceful_without_tesseract():
    """Verify try_ocr_region returns None when pytesseract is not installed."""
    canvas = np.ones((50, 200, 3), dtype=np.uint8) * 200
    result = try_ocr_region(canvas)
    # Should return None or a string — never crash
    assert result is None or isinstance(result, str)


def test_load_image_from_bytes_invalid():
    """Verify that load_image_from_bytes raises ValueError for corrupt data."""
    corrupt = b"THIS_IS_NOT_AN_IMAGE_AT_ALL"
    try:
        load_image_from_bytes(corrupt)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Failed to decode" in str(e)


def test_load_image_from_bytes_valid():
    """Verify that load_image_from_bytes decodes a valid in-memory PNG."""
    synth = np.zeros((80, 80, 3), dtype=np.uint8)
    cv2.rectangle(synth, (5, 5), (75, 75), (0, 255, 0), -1)
    _, encoded = cv2.imencode(".png", synth)
    raw = encoded.tobytes()

    decoded = load_image_from_bytes(raw)
    assert decoded.shape == (80, 80, 3)

