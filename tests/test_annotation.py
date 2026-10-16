"""Unit tests for visual annotations and image processing.

Owned by: MEMBER 2 (Computer Vision)
"""

import numpy as np
from src.eagle_eye.vision.annotation import draw_bounding_box, draw_issue_marker
from src.eagle_eye.vision.image_processor import resize_image_aspect_ratio, extract_crop


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
